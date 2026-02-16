import os

MODEL_NAME = os.getenv("CHATLEGALGPT_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
EMBED_MODEL_NAME = os.getenv("CHATLEGALGPT_EMBED", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

FAISS_INDEX_PATH = os.getenv("CHATLEGALGPT_FAISS_INDEX", "../indexes/faiss.index")
DOCSTORE_PATH = os.getenv("CHATLEGALGPT_DOCSTORE", "../indexes/docstore.jsonl")

TOP_K = int(os.getenv("CHATLEGALGPT_TOP_K", "5"))
MAX_NEW_TOKENS = int(os.getenv("CHATLEGALGPT_MAX_NEW_TOKENS", "512"))

# CORS (pour l'UI)
CORS_ORIGINS = os.getenv("CHATLEGALGPT_CORS_ORIGINS", "http://localhost:5173").split(",")

# Safety
MAX_QUESTION_CHARS = int(os.getenv("CHATLEGALGPT_MAX_QUESTION_CHARS", "2000"))
