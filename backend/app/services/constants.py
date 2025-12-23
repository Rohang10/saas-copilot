import os

MIN_SIMILARITY_SCORE = float(os.getenv("MIN_SIMILARITY_SCORE", 0.15))
MIN_CHUNKS_REQUIRED = int(os.getenv("MIN_CHUNKS_REQUIRED", 1))
TOP_K_DEFAULT = int(os.getenv("TOP_K_DEFAULT", 5))
