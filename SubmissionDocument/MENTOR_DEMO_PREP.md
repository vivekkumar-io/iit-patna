# Mentor Demo Preparation Guide

**Project:** Enterprise Knowledge Assistant with Advanced RAG  
**Author:** Vivek Kumar  
**Program:** IIT Patna — GenAI Development Program (Project 2)  
**Company:** Oeeggis Corporation (fictional — academic project)

Use this document to prepare for your mentor demo. It covers architecture, code walkthrough, demo script, and likely technical questions with answers based on your actual implementation.

---

## Table of Contents

1. [30-Second Elevator Pitch](#1-30-second-elevator-pitch)
2. [Architecture Overview](#2-architecture-overview)
3. [Project Structure](#3-project-structure)
4. [Code Deep Dive](#4-code-deep-dive)
5. [Configuration Reference](#5-configuration-reference)
6. [Demo Script (Step by Step)](#6-demo-script-step-by-step)
7. [Technical Q&A — Must Know](#7-technical-qa--must-know)
8. [Advanced / Tough Questions](#8-advanced--tough-questions)
9. [Limitations (Be Honest)](#9-limitations-be-honest)
10. [Quick Cheat Sheet](#10-quick-cheat-sheet)

---

## 1. 30-Second Elevator Pitch

> "I built an Enterprise Knowledge Assistant for Oeeggis Corporation — a fictional company for this academic project. Employees can ask questions about HR, IT, travel, and benefits policies in natural language. The system uses **Advanced RAG**: documents are chunked and indexed into **ChromaDB** (vector) and **BM25** (keyword). At query time, both searches run, results are merged with **RRF**, then a **cross-encoder reranker** picks the best 5 chunks. The **LLM** generates a grounded answer with **source citations**. It also handles **follow-up questions** using chat memory and skips document search for greetings and casual introductions."

---

## 2. Architecture Overview

### A. Indexing Pipeline (Offline — run once)

```
Documents (PDF / TXT / DOCX)
        │
        ▼
  Document Loader          ← ingestion/loader.py
        │
        ▼
     Chunker               ← ingestion/chunker.py (600 chars, 120 overlap)
        │
        ▼
   Embeddings              ← OpenAI text-embedding-3-small
        │
        ├──────────────────────┐
        ▼                      ▼
  ChromaDB Vector Store    BM25 Index (pickle)
  data/vector_store/       data/bm25_index/
```

**Command:** `python scripts/ingest.py`

### B. Query Pipeline (Online — when user asks)

```
User Query (Streamlit)
        │
        ▼
  Route Message            ← Greeting? Intro? Policy question?
        │
        ├─ Greeting ──────────────► Fixed reply (no search)
        ├─ Casual intro ──────────► Instant regex reply (no search)
        │
        └─ Policy question
                │
                ▼
        Memory Rewrite         ← "What about carry-forward?" → standalone query
                │
                ▼
        Vector Search (k=15) + BM25 Search (k=15)
                │
                ▼
        RRF Merge (k=60)       ← Reciprocal Rank Fusion
                │
                ▼
        Cross-Encoder Rerank   ← Top 5 chunks
                │
                ▼
        Context Builder        ← Format chunks for LLM
                │
                ▼
        LLM (gpt-4o-mini)      ← Generate answer
                │
                ▼
        Source Citations + Chat Memory
                │
                ▼
        Streamlit UI
```

### C. Query Routing (4 Paths)

| Route | Example | What Happens | Retrieval? | LLM? |
|-------|---------|--------------|------------|------|
| **Greeting** | "Hi", "Hello" | Fixed welcome message | No | No |
| **Casual intro** | "Hi, I'm Abhishek from Bangalore" | Regex extracts name/city | No | No |
| **Memory question** | "What is my name?" | Answers from chat history | No | No |
| **Policy question** | "What is the VPN policy?" | Full RAG pipeline | Yes | Yes |

**Routing logic lives in:**
- `app/ui/chat.py` — greeting detection
- `generation/chain.py` — `should_search_documents()` and `build_instant_conversational_reply()`

---

## 3. Project Structure

```
Enterprise_Knowledge_Assistant/
├── app/
│   ├── main.py              # Streamlit entry point
│   ├── config.py            # All settings (chunk size, models, paths)
│   └── ui/
│       ├── bootstrap.py     # Preload models at startup
│       ├── chat.py          # Chat UI + routing
│       ├── session.py       # Chat history + reset
│       └── sidebar.py       # Knowledge Scope list
├── ingestion/
│   ├── loader.py            # Load PDF/DOCX/TXT
│   ├── chunker.py           # Split into chunks
│   ├── embedder.py          # OpenAI embeddings
│   └── pipeline.py          # Full ingest orchestration
├── retrieval/
│   ├── vector_store.py      # ChromaDB load/save
│   ├── hybrid_retriever.py  # Vector + BM25 + RRF + rerank
│   ├── reranker.py          # Cross-encoder scoring
│   └── retriever.py         # KnowledgeRetriever facade
├── generation/
│   ├── chain.py             # Main RAG orchestration (RAGChain.ask)
│   ├── memory.py            # Conversation history (5 turns)
│   ├── prompt.py            # System + context + rewrite prompts
│   └── guard.py             # Context formatting + source list
├── scripts/
│   └── ingest.py            # CLI indexing
├── data/
│   ├── documents/           # Input policy files
│   ├── vector_store/        # ChromaDB (generated)
│   └── bm25_index/          # BM25 pickle (generated)
└── logs/                    # Debug logs per session
```

---

## 4. Code Deep Dive

### 4.1 Ingestion — `ingestion/pipeline.py`

**Function:** `run_ingestion()`

| Step | What | File |
|------|------|------|
| 1 | Load all PDF/DOCX/TXT from `data/documents/` | `loader.py` |
| 2 | Split into chunks (600 chars, 120 overlap) | `chunker.py` |
| 3 | Embed chunks → save to ChromaDB | `embedder.py` + Chroma |
| 4 | Build BM25 index → save as pickle | `BM25Retriever` |

**Chunk settings** (`app/config.py`):
- `chunk_size = 600` characters
- `chunk_overlap = 120` characters (20% overlap keeps context across chunk boundaries)

**Why character-based chunking?** Simple and works well for policy text. Tradeoff: not token-aware (600 chars ≠ 600 tokens).

---

### 4.2 Retrieval — `retrieval/hybrid_retriever.py`

**Function:** `HybridRetriever.retrieve(question)`

| Step | Action | Count |
|------|--------|-------|
| 1 | Vector search (ChromaDB, semantic similarity) | top **15** |
| 2 | BM25 keyword search (exact term matching) | top **15** |
| 3 | RRF merge both lists | deduplicated |
| 4 | Cross-encoder rerank | top **5** sent to LLM |

**RRF Formula** (`combine_search_results`):
```
score += 1.0 / (k + rank + 1)    where k = 60
```
Each chunk gets a score from both lists. Higher combined score = better rank.

**Why hybrid?**
- **Vector search** catches meaning: "work from home" matches "remote work policy"
- **BM25** catches exact terms: "VPN", "carry-forward", "sick days"
- **RRF** merges without needing to normalize different score scales

**Why rerank?**
- Initial retrieval optimizes **recall** (find many candidates)
- Cross-encoder reranker optimizes **precision** (pick best 5 for LLM context)

**Reranker model:** `cross-encoder/ms-marco-MiniLM-L-6-v2` (runs locally via sentence-transformers)

---

### 4.3 Generation — `generation/chain.py`

**Main class:** `RAGChain`  
**Main method:** `ask(user_question)`

**Policy question flow inside `ask()`:**

```
Step 1: rewrite_follow_up_question()
        → Uses LLM + chat history to make follow-ups standalone
        → Example: "What about carry-forward?" → "What is the leave carry-forward policy?"

Step 2: retriever.retrieve(rewritten_question)
        → Hybrid search + rerank

Step 3: If no chunks found
        → Return safe message: "I could not find this information..."

Step 4: format_context_for_llm(chunks)
        → Labels each chunk with source filename

Step 5: generate_answer_from_context()
        → LLM with SYSTEM_PROMPT + CONTEXT_PROMPT + chat history

Step 6: get_source_list()
        → Deduped filenames for UI citations

Step 7: chat_memory.add_turn()
        → Save Q&A for future follow-ups
```

**Routing function:** `should_search_documents(user_message)`

Returns **False** (skip retrieval) when:
- Message contains memory phrases: `"my name"`, `"who am i"`, `"where am i from"`, etc.

Returns **True** (run RAG) when:
- Message contains `?`
- OR contains policy keywords: `policy`, `leave`, `vpn`, `salary`, `travel`, etc.
- OR contains question phrases: `"what is"`, `"how many"`, `"tell me"`, etc.

**Instant reply:** `build_instant_conversational_reply()` uses regex to extract name/location — no LLM call, fast and safe.

---

### 4.4 Prompts — `generation/prompt.py`

**SYSTEM_PROMPT** — Core rules for the LLM:
1. Answer only from document context + conversation history
2. Do NOT use outside knowledge
3. If answer not found → say exact not-found message
4. Do NOT invent numbers, dates, or policies

**CONTEXT_PROMPT** — Template for final answer:
- Injects: `{chat_history}`, `{context}`, `{question}`

**REWRITE_CHAIN_PROMPT** — Used to rewrite follow-up questions using memory

---

### 4.5 Hallucination Guard — `generation/guard.py` + prompts

**Three layers:**
1. **Prompt rules** — SYSTEM_PROMPT forbids outside knowledge
2. **Empty retrieval check** — `has_documents()` returns False → safe not-found message
3. **Source citations** — Only shown when real chunks were retrieved

**Not-found message:**
> "I could not find this information in the available documents."

---

### 4.6 UI — `app/ui/chat.py` + `bootstrap.py`

**Startup** (`bootstrap.py`):
- `@st.cache_resource` loads retriever once per server process
- `ensure_app_ready()` preloads ChromaDB + BM25 + reranker at startup
- First load takes 60–90 seconds (model download + warmup)

**Chat flow** (`chat.py`):
1. User types question → stored in `st.session_state.messages`
2. Greeting check → fixed reply
3. `should_search_documents()` → instant reply OR full RAG
4. Answer + sources displayed below assistant message
5. "Clear / Reset" → clears memory, models stay loaded

**Memory:**
- Last **5 turns** (10 messages) kept in `InMemoryChatMessageHistory`
- Lost on server restart (not persisted to database)

---

## 5. Configuration Reference

| Setting | Default | Purpose |
|---------|---------|---------|
| `llm_model` | `gpt-4o-mini` | Answer + rewrite |
| `embedding_model` | `text-embedding-3-small` | Vector embeddings |
| `reranker_model` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Reranking |
| `chunk_size` | 600 | Characters per chunk |
| `chunk_overlap` | 120 | Overlap between chunks |
| `retrieval_top_k` | 15 | Candidates per search (vector + BM25) |
| `rerank_top_n` | 5 | Chunks sent to LLM |
| `memory_window` | 5 | Chat turns remembered |
| LLM temperature | 0.1 | Low randomness for factual answers |
| RRF constant | 60 | Hardcoded in hybrid_retriever.py |

All configurable via `.env` file (see `.env.example`).

---

## 6. Demo Script (Step by Step)

### Before Demo
1. Run `setup.bat` (first time only)
2. Add `OPENAI_API_KEY` in `.env`
3. Run `python scripts/ingest.py` (if indexes missing)
4. Run `start.bat` → wait for preload spinner to finish
5. Open `http://localhost:8501`

### Demo Sequence

| # | You Say / Do | What to Explain |
|---|--------------|-----------------|
| 1 | Show PPT Slide 4 (flow diagram) | "This is the full architecture — indexing offline, query online" |
| 2 | Show sidebar "Knowledge Scope" | "These are the indexed policy documents" |
| 3 | Type: **"Hi"** | "Greeting path — fixed reply, no API cost, no retrieval" |
| 4 | Type: **"Hi, my name is Abhishek from Bangalore"** | "Casual intro — regex extracts name/city, instant reply, no RAG" |
| 5 | Type: **"What is the VPN policy?"** | "Full RAG — hybrid search, rerank, LLM answer + IT_Policy.txt source" |
| 6 | Type: **"What about reimbursement?"** | "Follow-up — memory rewrite makes this a standalone search query" |
| 7 | Type: **"What is my name?"** | "Memory question — answered from chat history, no document search" |
| 8 | Type: **"What is the salary for the CEO?"** | "Hallucination guard — not in docs, safe not-found message" |
| 9 | Click **Clear / Reset** | "Memory cleared; models stay loaded for next question" |
| 10 | (Optional) Open `logs/` folder | "Full trace: rewrite prompt, retrieved chunks, LLM response" |

### If Something Goes Slow
- Say: "First startup loads ChromaDB, BM25, and cross-encoder reranker — takes about 60–90 seconds once."
- After warmup, answers should be faster.

---

## 7. Technical Q&A — Must Know

### RAG Basics

**Q: What is RAG?**  
A: Retrieval-Augmented Generation. Instead of asking the LLM to answer from memory, we first **retrieve** relevant document chunks, then **augment** the prompt with that context, then **generate** the answer. This grounds answers in real company documents.

**Q: Why not fine-tune the LLM on company docs?**  
A: Fine-tuning is expensive, hard to update when policies change, and risks the model memorizing outdated info. RAG lets us update documents and re-ingest without retraining.

**Q: What is chunking and why?**  
A: Large documents are split into smaller pieces (600 chars) so search can find the most relevant section, not the whole document. Overlap (120 chars) prevents losing context at chunk boundaries.

---

### Hybrid Search

**Q: Why hybrid search instead of vector-only?**  
A: Vector search is good for semantic similarity ("work from home" ≈ "remote policy") but can miss exact terms. BM25 is good for exact keywords ("VPN", "carry-forward"). Combining both gives better coverage.

**Q: What is RRF?**  
A: Reciprocal Rank Fusion. Merges two ranked lists without normalizing scores. Formula: `score += 1/(k + rank + 1)` with k=60. A chunk appearing in both lists gets a higher combined score.

**Q: Why rerank after retrieval?**  
A: Vector + BM25 are fast but approximate (bi-encoder). Cross-encoder reranker scores each (question, chunk) pair together — more accurate but slower. We retrieve 15+15 broadly, then rerank to top 5 precisely.

**Q: How many chunks go to the LLM?**  
A: 5 chunks after reranking (`rerank_top_n = 5`).

---

### Models

**Q: Which LLM do you use?**  
A: `gpt-4o-mini` via OpenAI API at temperature 0.1 (low randomness for factual answers).

**Q: Which embedding model?**  
A: `text-embedding-3-small` via OpenAI API. Used at ingest time and query time for vector search.

**Q: Which reranker?**  
A: `cross-encoder/ms-marco-MiniLM-L-6-v2` from Hugging Face, runs locally via sentence-transformers. Downloaded on first run.

**Q: Why gpt-4o-mini and not GPT-4?**  
A: Cost-effective for academic project. Good enough for policy Q&A with grounded context. Temperature 0.1 keeps answers factual.

---

### Memory & Follow-ups

**Q: How do you handle follow-up questions?**  
A: `rewrite_follow_up_question()` uses LangChain `RunnableWithMessageHistory` with an LLM to rewrite "What about carry-forward?" into a standalone query like "What is the leave carry-forward policy?" before retrieval.

**Q: How much history is kept?**  
A: Last 5 turns (`memory_window = 5`). Implemented as max 10 messages in `ChatMemory`.

**Q: Is memory persisted?**  
A: No. In-memory only (`InMemoryChatMessageHistory`). Lost on server restart. Clear/Reset button clears it manually.

---

### Hallucination & Safety

**Q: How do you prevent hallucination?**  
A: Three layers: (1) strict SYSTEM_PROMPT rules, (2) empty-retrieval safe message via `has_documents()`, (3) source citations only from retrieved chunks.

**Q: What if the LLM still hallucinates?**  
A: Honest answer: prompt-based guard is not 100% foolproof. A production system would add a verification step or confidence scoring. For this project, empty-retrieval fallback + strict prompts handle most cases.

**Q: What happens when info is not in documents?**  
A: Returns: "I could not find this information in the available documents." with no source citations.

---

### Architecture & Design

**Q: Why Streamlit and not FastAPI + React?**  
A: Streamlit is faster to build for a chat demo. Single Python file UI, no separate frontend. Good for academic prototype.

**Q: Why lazy loading / preload?**  
A: ChromaDB + BM25 + reranker are heavy. `@st.cache_resource` loads once per server process. `ensure_app_ready()` warms up at startup so first user question isn't slow.

**Q: Why separate ingestion and query pipelines?**  
A: Indexing is expensive (embed all chunks once). Query is fast (search existing index). Standard RAG pattern — ingest offline, query online.

**Q: Where are indexes stored?**  
A: ChromaDB → `data/vector_store/` (SQLite). BM25 → `data/bm25_index/bm25_retriever.pkl`.

---

### Code-Specific

**Q: What is `should_search_documents()`?**  
A: Routing gate in `generation/chain.py`. Returns True only when the message looks like a policy/document question. Prevents unnecessary retrieval for intros and memory questions.

**Q: What is `format_context_for_llm()`?**  
A: In `generation/guard.py`. Converts retrieved chunks into labeled text blocks: `[IT_Policy.txt]\nchunk text\n\n---\n\n[next chunk]`.

**Q: What document formats are supported?**  
A: PDF (PyPDFLoader), DOCX (Docx2txtLoader), TXT (TextLoader UTF-8). Unsupported files are skipped with a log entry.

**Q: How are sources shown in UI?**  
A: `get_source_list()` dedupes filenames. `show_sources()` in chat.py renders HTML bullet list under the answer.

---

## 8. Advanced / Tough Questions

**Q: Why chunk size 600 and not 1000 or 512 tokens?**  
A: 600 characters is a practical middle ground — small enough for precise retrieval, large enough to hold a policy paragraph. Overlap of 120 (20%) prevents splitting mid-sentence. Token-based chunking would be more accurate but adds complexity.

**Q: What is the difference between bi-encoder and cross-encoder?**  
A: Bi-encoder (embeddings) encodes query and document separately — fast but less accurate. Cross-encoder scores (query, document) together — slower but more accurate. We use bi-encoder for initial retrieval, cross-encoder for reranking.

**Q: Can two users use the app at the same time?**  
A: Streamlit shares one server process. `@st.cache_resource` retriever is shared (good). But `RAGChain` and memory are per-session. Multiple users would have separate chat histories but share the same loaded models.

**Q: How would you scale this for production?**  
A: Replace Streamlit with FastAPI + React, add user auth, persist memory to Redis/DB, use a managed vector DB (Pinecone/Weaviate), add async ingestion pipeline, monitoring, and rate limiting.

**Q: What if a new policy document is added?**  
A: Place file in `data/documents/`, re-run `python scripts/ingest.py`. Full re-index (no incremental update in current design).

**Q: Why is Knowledge Scope in sidebar display-only?**  
A: The filtering code exists (`_filter_by_sources`) but UI always passes all documents. Could be extended with checkboxes for per-document search.

**Q: What is the cost per query?**  
A: Roughly: 1 embedding call (query) + 1 LLM call (rewrite, if follow-up) + 1 LLM call (answer). Embedding at ingest is one-time per chunk. gpt-4o-mini and text-embedding-3-small are low-cost models.

**Q: How do you evaluate RAG quality?**  
A: For this project: manual testing with sample questions, checking source citations, testing not-found cases. Production would use metrics like faithfulness, answer relevance, and retrieval recall.

**Q: What is LangChain's role here?**  
A: Provides document loaders, text splitters, Chroma integration, BM25 retriever, chat memory (`RunnableWithMessageHistory`), and OpenAI wrappers. We orchestrate the pipeline ourselves in `chain.py`.

---

## 9. Limitations (Be Honest)

| Limitation | What to Say |
|------------|-------------|
| Requires OpenAI API key | Paid usage for embeddings + chat |
| Slow first startup | 60–90 sec model load; one-time per server start |
| In-memory memory only | Not persisted; lost on restart |
| No user authentication | Anyone with URL can query all docs |
| Prompt-based guard only | Not 100% hallucination-proof |
| Full re-ingest on doc change | No incremental indexing |
| English only | Models and docs assume English |
| No streaming | Full response returned at once |

**Good line for mentor:**  
> "These are known tradeoffs for an academic prototype. In production I would add auth, persistent memory, incremental indexing, and a stronger verification layer."

---

## 10. Quick Cheat Sheet

```
CHUNK:     600 chars, 120 overlap
RETRIEVE:  15 vector + 15 BM25 → RRF (k=60) → rerank top 5
LLM:       gpt-4o-mini, temp 0.1
EMBED:     text-embedding-3-small
RERANKER:  cross-encoder/ms-marco-MiniLM-L-6-v2
MEMORY:    5 turns, in-memory
VECTOR DB: ChromaDB → data/vector_store/
KEYWORD:   BM25 pickle → data/bm25_index/
INGEST:    python scripts/ingest.py
RUN APP:   start.bat → localhost:8501
NOT FOUND: "I could not find this information in the available documents."

ROUTING:
  Greeting      → chat.py fixed reply
  Intro/Memory  → should_search_documents() = False → regex instant reply
  Policy Q      → full RAGChain.ask()

KEY FILES:
  chain.py          → RAG orchestration
  hybrid_retriever  → Vector + BM25 + RRF + rerank
  guard.py          → Context format + sources
  chat.py           → UI routing
  bootstrap.py      → Model preload
  config.py         → All settings
```

---

## Appendix: Sample Mentor Dialog

**Mentor:** "Walk me through what happens when I ask 'What is the leave policy?'"  
**You:** "The message goes to `chat.py`. It's not a greeting and `should_search_documents()` returns True because 'policy' is a keyword. It calls `RAGChain.ask()`. Step 1 rewrites the question using memory if needed. Step 2 runs hybrid retrieval — 15 vector results from ChromaDB, 15 BM25 results, merged with RRF, reranked to top 5. Step 3 formats those chunks with source labels. Step 4 sends context + question to gpt-4o-mini. Step 5 returns the answer with source filenames shown below the reply."

**Mentor:** "What if I ask something not in the documents?"  
**You:** "Retrieval returns no relevant chunks. `has_documents()` returns False. The system returns the safe not-found message without inventing an answer and without showing any sources."

**Mentor:** "Why hybrid and not just vector search?"  
**You:** "Policy documents have exact terms like 'VPN' or 'carry-forward' where BM25 excels. Vector search handles paraphrased questions like 'can I work from home'. RRF combines both ranked lists so we get the best of both."

---

**Good luck with your demo!**

*Author: Vivek Kumar | IIT Patna — GenAI Development Program*
