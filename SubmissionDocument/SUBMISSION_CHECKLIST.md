# Submission Checklist — Enterprise Knowledge Assistant

**Author:** Vivek Kumar  
**Project:** Project 2 — Enterprise Knowledge Assistant with Advanced RAG  
**Use this checklist before final submission. Tick each box only after you verify it.**

---

## How to use this document

1. Go through each section in order.
2. Mark `[x]` when verified, leave `[ ]` if not done.
3. Fix all items marked **FIX REQUIRED** before submitting.
4. Run the **Final Demo Test** at the bottom at least once.

**Status legend**
- ✅ Ready
- ⚠️ Partial — needs improvement
- ❌ Not done — must fix before submit

---

## SECTION 1: Source Code

| # | Requirement | Status | Verified |
|---|-------------|--------|----------|
| 1.1 | Complete Python source code included | | [ ] |
| 1.2 | Proper project structure (`app/`, `ingestion/`, `retrieval/`, `generation/`, `util/`, `scripts/`) | | [ ] |
| 1.3 | Modular implementation (separate files per responsibility) | | [ ] |
| 1.4 | No unnecessary hard-coded values (settings in `app/config.py` + `.env`) | | [ ] |
| 1.5 | Clear variable and function names | | [ ] |
| 1.6 | `requirements.txt` included | | [ ] |
| 1.7 | Author name in Python files (`Author: Vivek Kumar`) | | [ ] |
| 1.8 | `.env.example` included with placeholder values | | [ ] |
| 1.9 | Real `.env` with API key **NOT** included in submission | | [ ] |
| 1.10 | `venv/`, `__pycache__/`, `logs/` excluded from zip (or empty) | | [ ] |

### Source code — quick checks

- [ ] `python scripts/ingest.py` runs without error
- [ ] `streamlit run app/main.py` opens the app
- [ ] No syntax errors in any `.py` file
- [ ] All imports work inside virtual environment

---

## SECTION 2: README.md

README must contain all of the following sections:

| # | Required section | Status | Verified |
|---|------------------|--------|----------|
| 2.1 | Project title | | [ ] |
| 2.2 | Problem statement | | [ ] |
| 2.3 | Solution overview | | [ ] |
| 2.4 | Architecture diagram | | [ ] |
| 2.5 | Technology stack | | [ ] |
| 2.6 | Project structure (folder tree) | | [ ] |
| 2.7 | Setup instructions | | [ ] |
| 2.8 | Environment variable requirements | | [ ] |
| 2.9 | How to run the application | | [ ] |
| 2.10 | Sample inputs | | [ ] |
| 2.11 | Sample outputs | | [ ] |
| 2.12 | Key design decisions | | [ ] |
| 2.13 | Limitations | | [ ] |
| 2.14 | Author name (Vivek Kumar) | | [ ] |

### README — content checklist

- [ ] Evaluator can set up project using README only (no extra instructions needed)
- [ ] Architecture flow is easy to understand
- [ ] OpenAI API key setup is clearly explained
- [ ] Ingestion step is documented before running the app

---

## SECTION 3: Sample Data

| # | Requirement | Status | Verified |
|---|-------------|--------|----------|
| 3.1 | Sample documents included in `data/documents/` | | [ ] |
| 3.2 | Evaluator can run app without creating data from scratch | | [ ] |
| 3.3 | At least **2 document formats** in sample data (PDF, DOCX, TXT) | | [ ] |
| 3.4 | Leave policy document included | | [ ] |
| 3.5 | HR handbook included | | [ ] |
| 3.6 | IT policy included | | [ ] |
| 3.7 | Travel policy included | | [ ] |
| 3.8 | Benefits documentation included | | [ ] |
| 3.9 | Code of conduct included | | [ ] |
| 3.10 | Company FAQs included | | [ ] |
| 3.11 | Sample outputs documented (README or `SAMPLE_OUTPUT.md`) | | [ ] |
| 3.12 | Optional: UI screenshots in `sample_output/screenshots/` | | [ ] |

### Sample documents — file checklist

Mark each file that exists in `data/documents/`:

- [ ] `Leave_Policy.pdf` (or `.txt`)
- [ ] `HR_Handbook.txt` (or `.docx`)
- [ ] `IT_Policy.txt`
- [ ] `Travel_Policy.txt`
- [ ] `Benefits_Documentation.txt`
- [ ] `Code_of_Conduct.docx` (or `.pdf`)
- [ ] `Company_FAQs.txt`

**Format count:** _____ formats present (need minimum **2**)

---

## SECTION 4: Assignment Functional Requirements (Project 2)

| # | Feature | Implementation file(s) | Verified |
|---|---------|------------------------|----------|
| 4.1 | Load documents from local folder | `ingestion/loader.py` | [ ] |
| 4.2 | Support 2+ document formats | `ingestion/loader.py` | [ ] |
| 4.3 | Split documents into chunks | `ingestion/chunker.py` | [ ] |
| 4.4 | Generate embeddings | `ingestion/embedder.py` | [ ] |
| 4.5 | Store embeddings in vector DB (ChromaDB) | `ingestion/pipeline.py` | [ ] |
| 4.6 | Basic vector/semantic retrieval | `retrieval/vector_store.py` | [ ] |
| 4.7 | Hybrid search (Vector + BM25) | `retrieval/hybrid_retriever.py` | [ ] |
| 4.8 | Reranking after retrieval | `retrieval/reranker.py` | [ ] |
| 4.9 | Conversational memory (follow-up questions) | `generation/chain.py` | [ ] |
| 4.10 | Source citations in answers | `generation/guard.py`, `app/ui/chat.py` | [ ] |
| 4.11 | Streamlit UI with chat | `app/main.py`, `app/ui/chat.py` | [ ] |
| 4.12 | Conversation history in UI | `app/ui/chat.py` | [ ] |
| 4.13 | Clear/reset conversation | `app/ui/sidebar.py` | [ ] |
| 4.14 | Display retrieved sources | `app/ui/chat.py` | [ ] |
| 4.15 | Basic error messages | `app/ui/chat.py` | [ ] |
| 4.16 | Hallucination handling / "not found" response | `generation/prompt.py`, `generation/chain.py` | [ ] |

---

## SECTION 5: General Submission Guidelines

| # | Guideline | Verified |
|---|-----------|----------|
| 5.1 | Implemented primarily in Python | [ ] |
| 5.2 | Runs locally on learner's system | [ ] |
| 5.3 | Uses GenAI frameworks from program (LangChain, RAG, etc.) | [ ] |
| 5.4 | No expensive/complex external infrastructure required | [ ] |
| 5.5 | OpenAI API used only if learner has access (optional paid service) | [ ] |
| 5.6 | Clean, modular, understandable code | [ ] |
| 5.7 | Demonstrates learner's own understanding | [ ] |
| 5.8 | Complete source code submitted | [ ] |
| 5.9 | Sample input data submitted | [ ] |
| 5.10 | Sample output submitted | [ ] |

---

## SECTION 6: Final Demo Test (run live before submit)

Run these steps in order and tick each box:

### Setup
- [ ] `setup.bat` OR `python -m venv venv` + `pip install -r requirements.txt` works
- [ ] `.env` file has valid `OPENAI_API_KEY`
- [ ] `python scripts/ingest.py` completes successfully
- [ ] Ingestion shows document count and chunk count

### App launch
- [ ] `start.bat` OR `streamlit run app/main.py` works
- [ ] App opens at **http://localhost:8501**
- [ ] Sidebar shows knowledge scope document list

### Test questions

| Test | Question | Expected result | Pass |
|------|----------|-----------------|------|
| T1 | "What is the leave policy?" | Answer from documents + sources listed | [ ] |
| T2 | "How many sick days do employees get?" | Correct answer with source | [ ] |
| T3 | (after T1) "What about carry-forward?" | Follow-up understood via memory | [ ] |
| T4 | "What is the VPN policy?" | Answer from IT policy + sources | [ ] |
| T5 | "What is the salary for CEO?" | "Could not find..." message | [ ] |

### UI features
- [ ] Chat history displays correctly
- [ ] Sources shown under assistant answers
- [ ] "Clear / Reset" button works
- [ ] Ingestion via `python scripts/ingest.py` documented and tested
- [ ] Error message shown if something fails (test by stopping API key temporarily)

### Logging
- [ ] Log file created in `logs/` folder
- [ ] Log contains step-by-step Python flow
- [ ] Log contains LLM prompts and responses

---

## SECTION 7: Files to include in submission zip

### Include ✅
- [ ] All `.py` source files
- [ ] `requirements.txt`
- [ ] `README.md`
- [ ] `SUBMISSION_CHECKLIST.md` (this file)
- [ ] `.env.example`
- [ ] `setup.bat` and `start.bat`
- [ ] `data/documents/` (all sample files)
- [ ] `SAMPLE_OUTPUT.md`
- [ ] `SubmissionDocument/` folder (evaluator docs)
- [ ] `sample_output/screenshots/` (optional)

### Do NOT include ❌
- [ ] `.env` (contains real API key)
- [ ] `venv/` folder
- [ ] `__pycache__/` folders
- [ ] `data/vector_store/` (evaluator will run ingest)
- [ ] `data/bm25_index/` (evaluator will run ingest)
- [ ] `logs/` folder

---

## SECTION 8: Final sign-off

| Item | Done |
|------|------|
| All **FIX REQUIRED** items resolved | [ ] |
| Final demo test (Section 6) passed | [ ] |
| README complete (Section 2) | [ ] |
| Sample data complete (Section 3) | [ ] |
| Submission zip prepared (Section 7) | [ ] |
| Project tested on a fresh run (setup → ingest → app) | [ ] |

---

**Submission ready?** Only check this when ALL sections above are complete:

- [ ] **I confirm this project is ready for submission.**

---

**Date validated:** _______________  
**Validated by:** Vivek Kumar

---

## Quick status summary (fill before submit)

| Area | Items done | Items total | % |
|------|------------|-------------|---|
| Source code | | 10 | |
| README | | 14 | |
| Sample data | | 12 | |
| Assignment features | | 16 | |
| Guidelines | | 10 | |
| Demo tests | | 15 | |
| **TOTAL** | | | |

**Notes / items still pending:**

```
1.
2.
3.
```
