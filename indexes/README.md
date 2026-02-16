# indexes/ (générés)

Ce dossier contient l’index vectoriel utilisé par le backend.

```mermaid
flowchart TB
  C["processed/chunks.jsonl"] --> B["build_index.py"]
  B --> I["faiss.index"]
  B --> D["docstore.jsonl"]
  I --> API["backend (retrieval)"]
  D --> API
```

Fichiers attendus :
- `faiss.index`
- `docstore.jsonl`

> Ces fichiers sont **générés** (souvent non versionnés).  
> Pour les produire : voir `data_pipeline/README.md`.
