# --- imports (ALL at top) ---
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.rag import router as rag_router
from app.db.session import engine, Base
from app.utils.logger import log_requests
from app.api.rag import ingest
import os

# --- environment loading ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --- database ---
Base.metadata.create_all(bind=engine)

# --- app ---
app = FastAPI(title="SaaS Support Copilot API")


@app.on_event("startup")
def run_ingestion_once():
    if os.getenv("AUTO_INGEST", "false").lower() == "true":
        ingest(x_admin_key=os.getenv("ADMIN_API_KEY"))


# --- middleware ---
app.middleware("http")(log_requests)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https://saas-copilot.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- routers ---
app.include_router(auth_router)
app.include_router(rag_router)


# --- health check ---
@app.get("/health")
def health():
    return {"status": "ok"}


# --- root endpoint ---
@app.get("/ready")
def ready():
    from app.services.vector_store import get_collection

    collection = get_collection()
    count = collection.count()

    return {
        "status": "ready" if count > 0 else "not_ready",
        "documents_indexed": count,
    }
