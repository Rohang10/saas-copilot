from fastapi import APIRouter, Header, HTTPException
from uuid import uuid4
import os

from app.utils.file_loader import load_docs
from app.services.chunking import chunk_text
from app.services.embeddings import embed_texts
from app.services.vector_store import (
    add_chunks,
    query_chunks,
    get_collection,
)
from app.services.llm import generate_answer
from app.services.prompt import build_prompt
from app.services.constants import (
    MIN_SIMILARITY_SCORE,
    MIN_CHUNKS_REQUIRED,
)
from app.services.safety import is_unsafe_question

router = APIRouter(prefix="/rag", tags=["RAG"])


# -----------------------------
# INGEST (Admin protected)
# -----------------------------
@router.post("/ingest")
def ingest(x_admin_key: str = Header(...)):
    if x_admin_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(status_code=403, detail="Forbidden")

    docs = load_docs()
    if not docs:
        raise HTTPException(status_code=500, detail="No documents found for ingestion")

    collection = get_collection()
    if collection.count() > 0:
        return {
            "status": "skipped",
            "message": "Documents already ingested",
            "documents_indexed": collection.count(),
        }

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["body"])
        if not chunks:
            continue

        embeddings = embed_texts([text for _, text in chunks])

        for (cid, text), embedding in zip(chunks, embeddings):
            all_chunks.append(
                {
                    "id": f"{doc['id']}_chunk_{cid}",
                    "text": text,
                    "embedding": embedding,
                    "meta": {
                        "doc_id": doc["id"],
                        "title": doc["title"],
                        "chunk_id": cid,
                    },
                }
            )

    if not all_chunks:
        raise HTTPException(status_code=500, detail="No chunks created during ingestion")

    add_chunks(all_chunks)

    return {
        "status": "ingested",
        "chunks": len(all_chunks),
    }


# -----------------------------
# ASK (RAG Query)
# -----------------------------
@router.post("/ask")
def ask(question: str, top_k: int = 5):
    trace_id = str(uuid4())

    if not question or len(question.strip()) < 5:
        return {
            "answer": "Please ask a clearer question.",
            "sources": [],
            "status": "invalid_input",
            "confidence": "low",
            "trace_id": trace_id,
        }

    if is_unsafe_question(question):
        return {
            "answer": "I cannot help with this request.",
            "sources": [],
            "status": "blocked",
            "confidence": "low",
            "trace_id": trace_id,
        }

    collection = get_collection()
    if collection.count() == 0:
        return {
            "answer": "Knowledge base is not initialized yet.",
            "sources": [],
            "status": "not_ready",
            "confidence": "low",
            "trace_id": trace_id,
        }

    query_embedding = embed_texts([question])[0]
    results = query_chunks(query_embedding, top_k)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        return {
            "answer": "I do not have enough information to answer this question.",
            "sources": [],
            "status": "low_context",
            "confidence": "low",
            "trace_id": trace_id,
        }

    context_chunks = []
    sources = []

    for doc, meta, dist in zip(documents, metadatas, distances):
        score = round(1 - dist, 3)

        if score >= MIN_SIMILARITY_SCORE:
            context_chunks.append(doc)
            sources.append(
                {
                    "chunk_text": doc,
                    "score": score,
                    "doc_id": meta["doc_id"],
                    "title": meta["title"],
                    "chunk_id": meta["chunk_id"],
                }
            )

    if len(context_chunks) < MIN_CHUNKS_REQUIRED:
        return {
            "answer": "I do not have enough reliable information to answer this question.",
            "sources": [],
            "status": "low_confidence",
            "confidence": "low",
            "trace_id": trace_id,
        }

    prompt = build_prompt(context_chunks, question)
    answer = generate_answer(prompt)

    if not answer or not answer.strip():
        return {
            "answer": "I do not have enough information to answer this question.",
            "sources": [],
            "status": "generation_failed",
            "confidence": "low",
            "trace_id": trace_id,
        }

    avg_score = sum(s["score"] for s in sources) / len(sources)

    confidence = (
        "low" if avg_score < 0.18 else
        "medium" if avg_score < 0.35 else
        "high"
    )

    return {
        "answer": answer,
        "sources": sources,
        "status": "ok",
        "confidence": f"{confidence}_confidence",
        "trace_id": trace_id,
    }
