from fastapi import APIRouter, Header, HTTPException
from uuid import uuid4
import os

from app.utils.file_loader import load_docs
from app.services.chunking import chunk_text
from app.services.embeddings import embed_texts
from app.services.vector_store import add_chunks, query_chunks
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
def ingest(x_admin_key: str = Header(None)):
    if x_admin_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(status_code=403, detail="Unauthorized")

    docs = load_docs()
    if not docs:
        return {"status": "error", "message": "No documents found"}

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["body"])
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
        return {"status": "error", "message": "No chunks created"}

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

    # Basic validation
    if not question or len(question.strip()) < 5:
        return {
            "answer": "Please ask a clearer question.",
            "sources": [],
            "status": "low_context",
            "confidence": "low",
            "trace_id": trace_id,
        }

    # Safety guard
    if is_unsafe_question(question):
        return {
            "answer": "I cannot help with this request.",
            "sources": [],
            "status": "blocked",
            "confidence": "low",
            "trace_id": trace_id,
        }

    # Embed + retrieve
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

    # Similarity filtering
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

    # Minimum evidence check
    if len(context_chunks) < MIN_CHUNKS_REQUIRED:
        return {
            "answer": "I do not have enough reliable information to answer this question.",
            "sources": [],
            "status": "low_confidence",
            "confidence": "low",
            "trace_id": trace_id,
        }

    # Build prompt and generate answer
    prompt = build_prompt(context_chunks, question)
    answer = generate_answer(prompt)

    if not answer or not answer.strip():
        return {
            "answer": "I do not have enough information to answer this question.",
            "sources": [],
            "status": "low_context",
            "confidence": "low",
            "trace_id": trace_id,
        }

    # Confidence calculation (based ONLY on retrieval)
    avg_score = sum(s["score"] for s in sources) / len(sources)

    if avg_score < 0.18:
        confidence = "low"
    elif avg_score < 0.35:
        confidence = "medium"
    else:
        confidence = "high"

    return {
        "answer": answer,
        "sources": sources,
        "status": "ok",
        "confidence": f"{confidence}_confidence",
        "trace_id": trace_id,
    }


# -----------------------------
# EVALUATION (Optional)
# -----------------------------
@router.post("/evaluate")
def evaluate():
    return {
        "retrieval_metrics": {
            "top_k_accuracy": "manual",
            "mean_similarity": "logged per request",
            "coverage": "sources_returned / top_k",
        },
        "generation_metrics": {
            "groundedness": "sources_used",
            "hallucination_rate": "manual review",
            "refusal_accuracy": "blocked / unsafe",
        },
        "note": "Use test questions + logs for evaluation",
    }
