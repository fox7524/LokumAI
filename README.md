# LokumAI

**Commercial-grade local AI chat studio** for macOS: a polished desktop UI + local MLX inference + persistent RAG + optional LoRA fine-tuning.

> Local-first by design: your chats, indexes, and adapters live on your machine.

---

## ✨ Key Features

**Chat experience**
- Desktop app built with **PyQt**
- Token streaming + Stop button
- Chat history persisted in SQLite

**RAG (Retrieval-Augmented Generation)**
- Index a folder (code/docs/PDF/DOCX/ZIM/optional OCR images)
- Persistent store on disk (survives restarts)
- Fast similarity search with **FAISS** + **sentence-transformers**

**Fine-tuning (MLX LoRA)**
- One-click training runner (subprocess via `mlx_lm lora`)
- Live logs + graceful stop
- Built-in dataset helpers (JSONL + SQLite)

---

## Table of Contents
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [RAG: persistent knowledge](#rag-persistent-knowledge)
- [LoRA fine-tuning](#lora-fine-tuning)
- [Dataset generation](#dataset-generation)
- [Project layout](#project-layout)
- [Troubleshooting](#troubleshooting)
- [Security](#security)

---

## Quickstart

### 1) Create + activate a virtualenv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

Optional OCR dependency (images):
```bash
brew install tesseract
```

### 3) Run
```bash
python3 -u main.py
```

Wait until the UI shows `Service: ready`.

---

## Configuration

### `prompts.json`
`prompts.json` controls:
- system prompt / user prompt
- theme
- model path (MLX model directory)
- RAG on/off

Key fields:
- `model_path`: local MLX model directory
- `use_rag`: enable/disable RAG

### Environment variables (advanced)

**RAG paths (persistent storage)**
- `LOKUMAI_HOME`: overrides the base app data folder (default: `~/.lokumai`)
- `LOKUMAI_RAG_DIR`: overrides the RAG store directory (default: `~/.lokumai/rag`)

**Fine-tune / memory shaping**
- `LOKUMAI_FT_MAX_SEQ_LENGTH` (default UI-driven)
- `LOKUMAI_FT_PRESPLIT` (`1` enables presplitting)
- `LOKUMAI_FT_PRESPLIT_CHARS_PER_TOKEN` (default `4.0`, lower = more aggressive split)
- `LOKUMAI_FT_CLEAR_CACHE_THRESHOLD` (lower = more frequent cache clears)

---

## RAG: persistent knowledge

RAG stores a cumulative index under the configured RAG directory.

Typical files:
- `faiss_index.bin` — vector index
- `docs_metadata.npy` — aligned chunk texts
- `chunks_meta.npy` — per-chunk metadata
- `rag_state.json` — per-file indexing state
- `rag_meta.json` — convenience metadata (e.g., last indexed folder)

**Reliability note**
- If the store is corrupted or fails to load, LokumAI quarantines the files (renames them with `.corrupt.<timestamp>`) instead of silently appearing empty. This prevents “it exists but doesn’t reload” confusion.

---

## LoRA fine-tuning

### Recommended starting point
For large models (e.g. 27B 6-bit), start conservative and scale up:
- `batch_size = 1`
- `max_seq_len = 384` (then try 512)
- avoid validation during training (run it after)

### Why training can OOM even with “free RAM”
On Apple Silicon, Metal memory can spike due to peak allocations + fragmentation. It’s normal to OOM while Activity Monitor still shows headroom.

---

## Dataset generation

### 1) Build a large behavior dataset from `prompts.json`
This repo includes a generator that reads your `system_prompt` and creates a **multi-turn** ChatML dataset that:
- asks questions only for **blocking unclear spots**
- continues immediately after the user answers (no looping)

```bash
python3 tools/build_prompt_dataset.py
```

Outputs:
- `lora_data/train.jsonl`
- `lora_data/valid.jsonl`

To change dataset size:
```bash
LOKUMAI_PROMPT_DATASET_SIZE=20000 python3 tools/build_prompt_dataset.py
```

---

## Project layout

Core modules:
- `main.py` — UI, streaming, chat persistence, Dev tools
- `rag_engine.py` — ingestion/index/search + persistence
- `file_ingest.py` — extraction + chunking (PDF/DOCX/ZIM/OCR/etc)
- `finetune_engine.py` — MLX LoRA subprocess + presplit
- `lokum_paths.py` — centralized path management (RAG dir overrides)

Data directories:
- `lora_data/` — datasets, adapters, configs, exports

---

## Troubleshooting

### Service: model path not found
- Set `model_path` in `prompts.json` to a valid local MLX model folder.

### RAG engine not available
- Ensure RAG deps are installed:
  - `pip install -r requirements.txt`
  - must include: `sentence-transformers`, `faiss-cpu`

### OCR returns empty text
- Install system `tesseract`:
  - `brew install tesseract`

---

## Security
- RAG indexes file content. Avoid indexing secrets (`.env`, API keys, credentials).
- Treat `app.db` and the RAG store as sensitive if they contain private data.
