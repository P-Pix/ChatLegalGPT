import os, json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

IN_PATH = os.getenv("IN_PATH", "../processed/chunks.jsonl")
INDEX_PATH = os.getenv("INDEX_PATH", "../indexes/faiss.index")
DOCSTORE_PATH = os.getenv("DOCSTORE_PATH", "../indexes/docstore.jsonl")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def main():
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    embedder = SentenceTransformer(EMBED_MODEL_NAME)

    texts = []
    docs = []
    with open(IN_PATH, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            texts.append(d["text"])
            docs.append(d)

    embs = embedder.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=True)
    embs = np.array(embs, dtype="float32")

    dim = embs.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine via normalized + inner product
    index.add(embs)

    faiss.write_index(index, INDEX_PATH)

    with open(DOCSTORE_PATH, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("OK:", INDEX_PATH, DOCSTORE_PATH, "vectors:", index.ntotal)

if __name__ == "__main__":
    main()
