.PHONY: help backend frontend pipeline docker-up docker-down serverless-offline finetune-ds

help:
	@echo "Targets:"
	@echo "  backend            - Lance l'API FastAPI en local"
	@echo "  frontend           - Lance l'UI React (Vite) en local"
	@echo "  pipeline           - Chunking + build index FAISS (exemple)"
	@echo "  docker-up          - Lance le backend via Docker"
	@echo "  docker-down        - Stoppe les containers Docker"
	@echo "  serverless-offline - Lance serverless-offline (Lambda-like)"
	@echo "  finetune-ds        - Génère un dataset SFT synthétique"

backend:
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && uvicorn app:app --reload --port 8000

frontend:
	cd frontend && npm install && npm run dev

pipeline:
	python data_pipeline/preprocess.py && python data_pipeline/build_index.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

serverless-offline:
	cd serverless && npm install && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && npx serverless offline --stage local

finetune-ds:
	python finetune/make_sft_dataset.py --chunks processed/chunks.jsonl --out datasets/sft_train.jsonl --n 2000
