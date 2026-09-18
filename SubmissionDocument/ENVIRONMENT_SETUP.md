# Environment Setup Guide

**Author:** Vivek Kumar

---

## Step 1 — Clone or extract project

```bat
git clone https://github.com/vivekkumar-io/iit-patna.git
cd iit-patna
```

Or open the extracted project folder in your terminal.

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
| `RETRIEVAL_TOP_K` | `8` |
| `RERANK_CANDIDATE_MAX` | `12` |
| `RERANK_TOP_N` | `5` |
| `MEMORY_WINDOW` | `5` |
| `SHOW_WELCOME_PAGE` | `true` |

---

## Deployment note

This project runs **locally** on your machine. There is no cloud-hosted public URL. After startup, open **http://localhost:8501** in your browser.

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

On first launch:
1. Review the **welcome page**
2. Click **Start Conversation**
3. Ask policy questions in the chat input

To rebuild indexes after document changes, run `reindex.bat`.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8501 in use | Run `start.bat` (kills old process) |
| Missing API key | Set `OPENAI_API_KEY` in `.env` |
| Index not found | Run `python scripts\ingest.py` |
| Slow first startup | Normal — models preload once |
