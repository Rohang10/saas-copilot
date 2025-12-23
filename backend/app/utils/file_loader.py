import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOCS_PATH = BASE_DIR / "data" / "docs"

def load_docs():
    docs = []
    for file in DOCS_PATH.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            docs.extend(json.load(f))
    return docs
