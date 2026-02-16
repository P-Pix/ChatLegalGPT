# Fine-tuning LoRA (SFT) pour ChatLegalGPT (optionnel)

## Schéma

```mermaid
flowchart LR
  D[(Dataset SFT JSONL)] --> T[train_lora.py\nTRL/PEFT]
  T --> A[(Adapter LoRA)]
  A --> I[Inference\n(base LLM + LoRA)]
  I --> B[Backend RAG (optionnel)\ncharger LoRA]
```


Objectif : améliorer le **format**, la **discipline** (refus quand sources insuffisantes), et le style de réponse.
On ne cherche PAS à mémoriser tout le droit : le RAG reste la source de vérité.

## Pré-requis
GPU recommandé (>= 16GB VRAM). CPU possible mais lent.

## Installation
```bash
cd finetune
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Dataset (JSONL)
Chaque ligne :
```json
{
  "instruction": "Question de l'utilisateur",
  "context": "[SOURCE 1] ...\nMETA: {...}\n\n[SOURCE 2] ...",
  "output": "Réponse structurée avec citations [SOURCE 1] ..."
}
```

Vous pouvez générer un dataset synthétique à partir de `processed/chunks.jsonl` via `make_sft_dataset.py`.

## Entraîner (LoRA)
```bash
python train_lora.py --model mistralai/Mistral-7B-Instruct-v0.3 --dataset ../datasets/sft_train.jsonl --out_dir ../models/chatlegalgpt-lora
```

## Inference avec LoRA
Dans `backend/config.py`, vous pouvez ajouter un chargement LoRA (exemple dans `lora_inference_example.py`).


## Contenu du dossier
- `train_lora.py` : entraînement LoRA SFT (TRL)
- `make_sft_dataset.py` : génération dataset synthétique depuis chunks
- `lora_inference_example.py` : exemple d’inférence base+LoRA
- `requirements.txt`
