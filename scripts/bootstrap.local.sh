#!/usr/bin/env bash
set -euo pipefail

# Bootstrap minimal pour lancer backend + frontend en local.
# Usage: bash scripts/bootstrap_local.sh

echo "==> Backend venv + deps"
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..

echo "==> Frontend deps"
cd frontend
npm install
cd ..

echo "OK. Lancement:"
echo "  Terminal 1: cd backend && source .venv/bin/activate && uvicorn app:app --reload --port 8000"
echo "  Terminal 2: cd frontend && npm run dev"
