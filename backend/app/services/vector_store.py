import chromadb
from chromadb.config import Settings
from pathlib import Path
import os

# -----------------------------
# Persistent storage path
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

CHROMA_PATH = os.getenv(
    "CHROMA_PERSIST_DIR",
    str(BASE_DIR / "chroma_db"),
)

# -----------------------------
# Global Chroma client (IMPORTANT)
# -----------------------------
_chroma_client = chromadb.Client(
    Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False,
    )
)

_COLLECTION_NAME = "saas_docs"


def get_collection():
    return _chroma_client.get_or_create_collection(
        name=_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(chunks: list[dict]):
    if not chunks:
        return

    collection = get_collection()

    collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[c["meta"] for c in chunks],
        ids=[c["id"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
    )

    # Explicit persistence
    _chroma_client.persist()


def query_chunks(query_embedding, top_k: int = 5):
    collection = get_collection()

    count = collection.count()
    print(f"VECTOR STORE COUNT: {count}")

    if count == 0:
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
