"""Handler Serverless (AWS Lambda style) pour FastAPI via Mangum.

Test local via serverless-offline:
- npx serverless offline --stage local

Remarque: en local, l'import du backend nécessite que le chemin soit correct.
On ajoute le dossier racine au sys.path pour réutiliser `backend/app.py`.
"""

import os
import sys
from mangum import Mangum

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Réutilise l'app FastAPI existante
from backend.app import app as fastapi_app  # noqa: E402

handler = Mangum(fastapi_app)
