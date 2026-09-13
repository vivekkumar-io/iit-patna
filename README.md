# Enterprise Knowledge Assistant

**Author:** Vivek Kumar  
**Program:** IIT Patna — GenAI Development Program (Final Evaluation)  
**Project:** Project 2 — Enterprise Knowledge Assistant with Advanced RAG

A production-oriented RAG application that lets employees ask questions about company policies using hybrid retrieval, reranking, conversational memory, and source-grounded answers.

> **Academic disclaimer:** This application is developed for educational purposes only. **Oeeggis Corporation** is a fictional organization. All documents in `data/documents/` are sample data created for this assignment and do not represent any real company or official policies.

---

## Problem Statement

Employees often need quick answers from HR, IT, travel, and benefits policies spread across multiple documents. Searching PDFs and text files manually is slow and inconsistent. This project solves that by building an **Employee Knowledge Assistant** that:

- Indexes local company documents
- Retrieves the most relevant content using advanced search
- Generates grounded answers with source citations
- Remembers follow-up questions in a chat interface

---

## Solution Overview

The application implements a full RAG pipeline:

1. **Ingest** documents from `data/documents/` (PDF, DOCX, TXT)
2. **Chunk** and **embed** text into ChromaDB
3. **Index** keyword data with BM25
4. At query time, run **hybrid search** (vector + BM25) with **reranking**
5. Send top chunks + conversation history to the LLM
6. Return an answer with **source citations** in the Streamlit UI

Casual introductions (name, city) are handled locally without document search. Policy questions trigger retrieval and grounded generation.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT UI (app/)                              │
│   Chat history │ Source citations │ Clear/Reset │ Knowledge scope        │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ user question
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      GENERATION LAYER (generation/)                      │
│  Conversational routing → Memory rewrite → Prompt → LLM → Guard          │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ search query
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      RETRIEVAL LAYER (retrieval/)                        │
│   Vector Search (ChromaDB)  +  BM25 Keyword Search  →  RRF Fusion      │
│                              →  Cross-Encoder Reranker                 │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ uses indexes built by
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER (ingestion/)                        │
│   Loader → Chunker → Embeddings → ChromaDB + BM25 index                  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
                          data/documents/  (sample policies)
```

### Query flow

```
User Question
    → Route (policy question vs casual intro)
    → Rewrite follow-up using chat memory
    → Hybrid retrieval (vector + BM25)
    → Reranking
    → Build context prompt
    → LLM answer
    → Sources displayed in UI
```

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| UI | Streamlit |
| Orchestration | LangChain |
| LLM | OpenAI `gpt-4o-mini` |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector DB | ChromaDB |
| Keyword search | BM25 (`rank-bm25`) |
| Reranking | `sentence-transformers` cross-encoder |
| Document loaders | PyPDF, python-docx, docx2txt |
| Config | `pydantic-settings`, `.env` |
| Logging | Custom file logger (`util/logger.py`) |

---

## Project Structure

```
Enterprise_Knowledge_Assistant/
├── app/                        # Streamlit application
│   ├── main.py                 # Entry point
│   ├── config.py               # Settings
│   └── ui/                     # Chat, sidebar, styles, bootstrap
├── ingestion/                  # Document loading, chunking, indexing
├── retrieval/                  # Vector store, BM25, hybrid, reranker
├── generation/                 # RAG chain, prompts, memory, guard
├── util/                       # Logging helpers
├── scripts/
│   └── ingest.py               # CLI ingestion
├── data/
│   └── documents/              # Sample company documents
├── SubmissionDocument/         # Submission package documents
├── ArchitectureDocument/       # Manual commands reference
├── requirements.txt
├── setup.bat                   # First-time setup (Windows)
├── start.bat                   # Clean + launch app (Windows)
├── .env.example
├── SAMPLE_OUTPUT.md
├── SUBMISSION_CHECKLIST.md
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Windows (batch scripts provided) or any OS with manual commands

### Option A — Windows batch scripts (recommended)

1. **First time only:** double-click `setup.bat`
2. Copy environment file:
   ```bat
   copy .env.example .env
   ```
3. Edit `.env` and add your OpenAI API key
4. Index documents:
   ```bat
   python scripts\ingest.py
   ```
5. Launch app:
   ```bat
   start.bat
   ```

### Option B — Manual setup

```bash
cd Enterprise_Knowledge_Assistant
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env
python scripts/ingest.py
streamlit run app/main.py
```

---

## Environment Variable Requirements

Copy `.env.example` to `.env` and configure:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | OpenAI API key for embeddings and chat |
| `LLM_MODEL` | No | `gpt-4o-mini` | Chat model |
| `EMBEDDING_MODEL` | No | `text-embedding-3-small` | Embedding model |
| `RERANKER_MODEL` | No | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Reranker |
| `CHUNK_SIZE` | No | `600` | Characters per chunk |
| `CHUNK_OVERLAP` | No | `120` | Chunk overlap |
| `RETRIEVAL_TOP_K` | No | `15` | Candidates before rerank |
| `RERANK_TOP_N` | No | `5` | Chunks sent to LLM |
| `MEMORY_WINDOW` | No | `5` | Conversation turns remembered |

**Never commit `.env` to GitHub.**

---

## How to Run the Application

1. Activate virtual environment
2. Ensure documents are indexed: `python scripts/ingest.py`
3. Start app: `start.bat` or `streamlit run app/main.py`
4. Open browser: **http://localhost:8501**
5. Wait for startup preload to finish, then ask questions

Re-run ingestion after adding or editing files in `data/documents/`.

---

## Sample Inputs

- "What is the leave policy?"
- "How many sick days do employees get?"
- "What about carry-forward?" (follow-up)
- "What is the VPN policy?"
- "What health insurance benefits are available?"
- "What is the travel reimbursement policy?"
- "What is the salary for the CEO?" (not-found test)
- "Hi, my name is Abhishek and I am from Bangalore." (intro, no policy search)

---

## Sample Outputs

See **[SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md)** for detailed example questions, expected answers, and source citations.

Brief example:

**Q:** What is the leave policy?  
**A:** Summary from leave policy documents.  
**Sources:** `Leave_Policy.pdf`

**Q:** What is the salary for the CEO?  
**A:** I could not find this information in the available documents.

---

## Key Design Decisions

1. **Hybrid retrieval** — Combines semantic search (ChromaDB) and keyword search (BM25) using reciprocal rank fusion for better recall on policy terms.
2. **Reranking** — Cross-encoder reranker improves precision before sending context to the LLM.
3. **Conversational routing** — Casual intros skip document retrieval to avoid irrelevant policy answers and reduce latency.
4. **Startup preload** — Vector store, BM25, and reranker load once at app startup so the first policy question is faster.
5. **Memory-aware rewrite** — Follow-up questions are rewritten using LangChain message history before retrieval.
6. **Hallucination guard** — Strict prompts and a fallback message when no relevant chunks are found.
7. **Modular layers** — Separate `ingestion`, `retrieval`, `generation`, and `app` packages for clarity and maintainability.

---

## Limitations

- Requires an OpenAI API key (paid usage for embeddings and chat).
- First startup can take 60–90 seconds while models load locally.
- Answers are limited to indexed documents in `data/documents/`.
- No user authentication or role-based access control.
- DOCX support depends on valid document files; corrupted files are skipped during ingestion.
- Conversation memory is session-based (in-memory), not persisted across server restarts.
- English-language documents and queries work best with the chosen models.

---

## Features Implemented (Assignment Mapping)

| Requirement | Implementation |
|-------------|----------------|
| Document ingestion (2+ formats) | `ingestion/loader.py` — PDF, DOCX, TXT |
| Chunking + embeddings + vector DB | `ingestion/chunker.py`, `embedder.py`, ChromaDB |
| Basic retrieval | `retrieval/vector_store.py` |
| Hybrid search | `retrieval/hybrid_retriever.py` |
| Reranking | `retrieval/reranker.py` |
| Conversational memory | `generation/memory.py`, `generation/chain.py` |
| Source citations | `generation/guard.py`, `app/ui/chat.py` |
| Streamlit UI | `app/main.py`, `app/ui/` |
| Hallucination handling | `generation/prompt.py`, `generation/chain.py` |

---

## Logging

Log files are created in `logs/` with step-by-step flow, retrieval details, LLM prompts, and responses.

---

## Submission Documents

Evaluator documents are collected in **`SubmissionDocument/`**:

- Submission index and checklist
- Architecture notes
- GitHub submission guide
- PowerPoint: `Enterprise_Knowledge_Assistant_Vivek_kumar.pptx`
- Architecture flow diagram (in `ARCHITECTURE.md` and submission PPT)
- Copies of `.env.example` and `SAMPLE_OUTPUT.md`

### Demo Video

**File:** `Demo_Enterprise_Knowledge_Assistant_video_with._Vivek_Kumar.mp4`  
**Google Drive:** _Add your link here_

> The demo video is not included in the GitHub repository due to file size. Upload to Google Drive and share the link in your submission.

**GitHub repo:** https://github.com/vivekkumar-io/iit-patna

---

## Author

**Vivek Kumar**  
IIT Patna — GenAI Development Program — Final Evaluation  
Project 2: Enterprise Knowledge Assistant with Advanced RAG
