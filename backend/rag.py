import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from config import (
    MODEL_NAME, EMBED_MODEL_NAME, FAISS_INDEX_PATH, DOCSTORE_PATH, TOP_K, MAX_NEW_TOKENS
)
from prompts import SYSTEM_PROMPT


def load_docstore(path: str):
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))
    return docs


class ChatLegalRAG:
    def __init__(self):
        self.embedder = SentenceTransformer(EMBED_MODEL_NAME)
        self.index = faiss.read_index(FAISS_INDEX_PATH)
        self.docs = load_docstore(DOCSTORE_PATH)

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )

    def retrieve(self, question: str, top_k: int = TOP_K):
        q_emb = self.embedder.encode([question], normalize_embeddings=True)
        q_emb = np.array(q_emb, dtype="float32")
        scores, idxs = self.index.search(q_emb, top_k)

        results = []
        for rank, i in enumerate(idxs[0]):
            if i < 0 or i >= len(self.docs):
                continue
            d = self.docs[i]
            results.append({
                "rank": rank + 1,
                "score": float(scores[0][rank]),
                "text": d["text"],
                "source": d.get("source", {}),
            })
        return results

    def generate(self, question: str):
        retrieved = self.retrieve(question)

        sources_block = "\n\n".join(
            [f"[SOURCE {r['rank']}] {r['text']}\nMETA: {json.dumps(r['source'], ensure_ascii=False)}"
             for r in retrieved]
        )

        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"Question: {question}\n\n"
            f"Extraits officiels:\n{sources_block}\n\n"
            "Réponse (avec des citations du type [SOURCE 1], [SOURCE 2], etc.) :"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        out = self.model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.2,
            top_p=0.9
        )
        text = self.tokenizer.decode(out[0], skip_special_tokens=True)

        # Heuristique: récupérer la fin du prompt
        if "Réponse" in text:
            answer = text.split("Réponse", 1)[-1].strip()
        else:
            answer = text.strip()

        return answer, retrieved
