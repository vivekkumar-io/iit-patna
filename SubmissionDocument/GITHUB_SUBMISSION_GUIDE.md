# GitHub Submission Guide

**Author:** Vivek Kumar  
**Repository:** https://github.com/vivekkumar-io/iit-patna

---

## Repository requirements (from evaluation document)

Your GitHub repository must include:

- [ ] Source code
- [ ] README
- [ ] Sample data
- [ ] `requirements.txt`
- [ ] `.env.example`
- [ ] Architecture diagram

**Never commit API keys, secrets, or the demo video file.**

---

## Demo video (Google Drive — NOT GitHub)

**File:** `Demo_Enterprise_Knowledge_Assistant_video_with._Vivek_Kumar.mp4`

Upload this video to **Google Drive** and share the link in:
- Your submission form
- `README.md` (Demo Video section)

The `.mp4` file is blocked by `.gitignore` and must not be pushed to GitHub.

---

## Recommended `.gitignore` (already configured)

```
.env
venv/
__pycache__/
*.pyc
logs/
data/vector_store/
data/bm25_index/
SubmissionDocument/*.mp4
```

---

## Steps to publish

```bash
cd Enterprise_Knowledge_Assistant
git init
git add .
git status
# Verify .env and *.mp4 are NOT listed
git commit -m "Final submission: Enterprise Knowledge Assistant RAG project"
git branch -M main
git remote add origin https://github.com/vivekkumar-io/iit-patna.git
git push -u origin main
```

---

## Pre-push checklist

- [ ] `.env` is NOT in `git status`
- [ ] No `.mp4` files in `git status`
- [ ] No `venv/` or `logs/` in `git status`
- [ ] `data/documents/` sample files are committed
- [ ] `README.md` is complete
- [ ] Google Drive link for demo video is ready for submission form
- [ ] `Enterprise_Knowledge_Assistant_Vivek_kumar.pptx` is committed

---

## Repository description (suggested)

> Enterprise Knowledge Assistant — Advanced RAG app with hybrid search, BM25, reranking, conversational memory, and Streamlit UI. IIT Patna GenAI Development Program — Final Evaluation (Project 2). Author: Vivek Kumar.
