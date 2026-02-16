"""Génère un dataset SFT (JSONL) à partir de chunks déjà prétraités.

Idée :
- On prend des chunks (extraits) comme contexte.
- On fabrique des questions génériques (templates) + on demande une réponse structurée avec citations.
- C'est un dataset "synthétique" pour apprendre le format.

Usage:
python make_sft_dataset.py --chunks ../processed/chunks.jsonl --out ../datasets/sft_train.jsonl --n 2000
"""

import argparse, json, random, os

TEMPLATES = [
    "Explique ce que dit ce texte et quels sont les points clés.",
    "Résume ce passage et précise les implications générales.",
    "Quels sont les éléments importants de ce texte ?",
    "Donne une explication simple de ce passage.",
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--chunks", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--n", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    random.seed(args.seed)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    chunks = []
    with open(args.chunks, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    if not chunks:
        raise RuntimeError("Aucun chunk trouvé.")

    with open(args.out, "w", encoding="utf-8") as out:
        for _ in range(args.n):
            c = random.choice(chunks)
            instruction = random.choice(TEMPLATES)
            context = f"[SOURCE 1] {c['text']}\nMETA: {json.dumps(c.get('source', {}), ensure_ascii=False)}"
            output = (
                "1) Résumé\n"
                "Ce passage décrit des dispositions juridiques et leurs éléments principaux. [SOURCE 1]\n\n"
                "2) Détails\n"
                "- Point clé 1 : à préciser selon le texte. [SOURCE 1]\n"
                "- Point clé 2 : à préciser selon le texte. [SOURCE 1]\n\n"
                "3) Ce qu'il manque / points à vérifier\n"
                "- Pour une situation concrète, il faut connaître le contexte factuel et les textes connexes. [SOURCE 1]\n\n"
                "4) Sources\n"
                "- " + json.dumps(c.get('source', {}), ensure_ascii=False) + "\n"
            )
            rec = {"instruction": instruction, "context": context, "output": output}
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print("OK:", args.out)

if __name__ == "__main__":
    main()
