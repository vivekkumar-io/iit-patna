# Submission Document Index

**Author:** Vivek Kumar  
**Project:** Project 2 — Enterprise Knowledge Assistant with Advanced RAG  
**Program:** IIT Patna — GenAI Development Program (Final Evaluation)

This folder contains all documents required for project submission and evaluation.

---

## Documents in this folder

| File | Purpose |
|------|---------|
| [INDEX.md](INDEX.md) | This index — start here |
| [README.md](README.md) | Full project README (copy for evaluators) |
| [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md) / [.docx](SAMPLE_OUTPUT.docx) | Example questions and expected outputs |
| [ARCHITECTURE.md](ARCHITECTURE.md) / [.docx](ARCHITECTURE.docx) | Architecture diagram and component flow |
| [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) / [.docx](ENVIRONMENT_SETUP.docx) | Environment variables and setup steps |
| [.env.example](.env.example) | Example environment file (no secrets) |
| [Enterprise_Knowledge_Assistant_Vivek_kumar.pptx](Enterprise_Knowledge_Assistant_Vivek_kumar.pptx) | Submission PowerPoint |
| [screenshots/app_home_screen.png](screenshots/app_home_screen.png) | Application UI screenshot |

### Demo video (Google Drive — not in GitHub)

**File name:** `Demo_Enterprise_Knowledge_Assistant_video_with._Vivek_Kumar.mp4`  
**Google Drive link:** _Add your link here before final submission_

> The demo video is **not** uploaded to GitHub (file size). Share the Google Drive link in your submission form and/or add it to `README.md`.

**Temp/work files** (video frames, narration segments, architecture HTML/PNG, draft PPTs, `DEMO_SCRIPT.md`, `MANUAL_COMMANDS.txt`) are stored at:
`D:\_GenAIProject\BKp\Enterprise_Knowledge_Assistant_temp`

---

## Related files in project root

| Path | Purpose |
|------|---------|
| `../README.md` | Main project README |
| `../SAMPLE_OUTPUT.md` | Sample outputs (copy) |
| `../requirements.txt` | Python dependencies |
| `../setup.bat` | First-time setup (Windows) |
| `../start.bat` | Clean + start app (Windows) |
| `../scripts/ingest.py` | Document indexing |
| `../data/documents/` | Sample input data |

---

## Quick start for evaluators

```bat
cd Enterprise_Knowledge_Assistant
setup.bat
copy .env.example .env
REM Edit .env and add OPENAI_API_KEY
python scripts\ingest.py
start.bat
```

Open: **http://localhost:8501**

---

## Submission checklist

**GitHub repo includes:**
- Source code, README, sample data, `requirements.txt`, `.env.example`, PPT, docs

**Submit separately (not on GitHub):**
- Demo video via **Google Drive link**: `Demo_Enterprise_Knowledge_Assistant_video_with._Vivek_Kumar.mp4`

**Never include:**
- `.env` (real API key)
- `venv/`, `__pycache__/`, `logs/`
- `data/vector_store/`, `data/bm25_index/`

---

**Prepared by:** Vivek Kumar
