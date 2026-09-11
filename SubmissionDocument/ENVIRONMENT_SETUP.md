# Environment Setup Guide

**Author:** Vivek Kumar

---

## Step 1 — Clone or extract project

```bat
cd D:\_GenAIProject\Enterprise_Knowledge_Assistant
```

---

## Step 2 — Create virtual environment

**Windows (easy):**
```bat
setup.bat
```

**Manual:**
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 3 — Configure environment variables

```bat
copy .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

Optional overrides:

| Variable | Default |
|----------|---------|
| `LLM_MODEL` | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | `text-embedding-3-small` |
| `RERANKER_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| `CHUNK_SIZE` | `600` |
| `CHUNK_OVERLAP` | `120` |
| `RETRIEVAL_TOP_K` | `15` |
| `RERANK_TOP_N` | `5` |
| `MEMORY_WINDOW` | `5` |

---

## Step 4 — Index documents

```bat
python scripts\ingest.py
```

Expected: documents loaded and chunks created.

---

## Step 5 — Run application

```bat
start.bat
```

Or:

```bat
streamlit run app/main.py
```

URL: **http://localhost:8501**

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8501 in use | Run `start.bat` (kills old process) |
| Missing API key | Set `OPENAI_API_KEY` in `.env` |
| Index not found | Run `python scripts\ingest.py` |
| Slow first startup | Normal — models preload once |
