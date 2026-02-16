import json
import os

IN_PATH = os.getenv("IN_PATH", "../raw/legifrance_dump.jsonl")
OUT_PATH = os.getenv("OUT_PATH", "../processed/chunks.jsonl")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))  # caractères
OVERLAP = int(os.getenv("OVERLAP", "150"))

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    text = " ".join(text.split())
    chunks = []
    i = 0
    while i < len(text):
        j = min(len(text), i + chunk_size)
        chunks.append(text[i:j])
        if j == len(text):
            break
        i = max(i + chunk_size - overlap, j)
    return chunks

def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    n = 0
    with open(IN_PATH, "r", encoding="utf-8") as fin, open(OUT_PATH, "w", encoding="utf-8") as fout:
        for line in fin:
            doc = json.loads(line)
            text = doc.get("text", "")
            src = doc.get("source", {})
            for k, ch in enumerate(chunk_text(text)):
                fout.write(json.dumps({
                    "text": ch,
                    "source": {**src, "chunk": k}
                }, ensure_ascii=False) + "\n")
                n += 1
    print(f"OK: wrote {n} chunks -> {OUT_PATH}")

if __name__ == "__main__":
    main()
