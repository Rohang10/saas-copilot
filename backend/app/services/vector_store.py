import chromadb
from chromadb.config import Settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CHROMA_PATH = BASE_DIR / "chroma_db"

settings = Settings(
    persist_directory=str(CHROMA_PATH),
    anonymized_telemetry=False,
)


def get_collection():
    client = chromadb.Client(settings)
    return client.get_or_create_collection(
        name="saas_docs",
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


def query_chunks(query_embedding, top_k: int = 5):
    collection = get_collection()

    print("COLLECTION COUNT:", collection.count())

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
