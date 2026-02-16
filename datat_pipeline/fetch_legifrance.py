"""Squelette d'ingestion Légifrance via PISTE (OAuth2).

⚠️ Vous devez :
- disposer d'un compte / application PISTE
- lire les CGU / quotas
- adapter les endpoints (codes, articles, etc.)

Variables d'env attendues :
- PISTE_TOKEN_URL
- PISTE_CLIENT_ID
- PISTE_CLIENT_SECRET
- LEGIFRANCE_API_BASE
- OUT_PATH (optionnel)
"""

import os
import json
import time
import requests

PISTE_TOKEN_URL = os.getenv("PISTE_TOKEN_URL")
PISTE_CLIENT_ID = os.getenv("PISTE_CLIENT_ID")
PISTE_CLIENT_SECRET = os.getenv("PISTE_CLIENT_SECRET")
LEGIFRANCE_API_BASE = os.getenv("LEGIFRANCE_API_BASE")

OUT_PATH = os.getenv("OUT_PATH", "../raw/legifrance_dump.jsonl")

def get_token():
    if not (PISTE_TOKEN_URL and PISTE_CLIENT_ID and PISTE_CLIENT_SECRET):
        raise RuntimeError("Variables PISTE_* manquantes.")
    resp = requests.post(
        PISTE_TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(PISTE_CLIENT_ID, PISTE_CLIENT_SECRET),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

def call_api(path, token, params=None):
    if not LEGIFRANCE_API_BASE:
        raise RuntimeError("LEGIFRANCE_API_BASE manquant.")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{LEGIFRANCE_API_BASE}{path}", headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()

def main():
    token = get_token()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    # TODO: Remplacer par un vrai parcours (pagination + endpoints)
    # Exemple générique:
    # for page in range(1, N):
    #     data = call_api("/endpoint", token, params={"page": page})
    #     ...

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        # placeholder (écrit un exemple pour valider le pipeline)
        example = {
            "text": "Article X — Exemple. Ceci est un exemple de texte juridique.",
            "source": {
                "origin": "legifrance_api",
                "id": "EXAMPLE-1",
                "title": "Exemple",
                "date": "2026-01-01",
                "url": "https://www.legifrance.gouv.fr"
            }
        }
        f.write(json.dumps(example, ensure_ascii=False) + "\n")

    time.sleep(0.1)

if __name__ == "__main__":
    main()
