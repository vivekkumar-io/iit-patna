"""
Preload assistant models from the command line before Streamlit starts.

Used by start.bat so startup progress appears in the console,
not as a blocking screen inside the web UI.

Author: Vivek Kumar
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SCRIPT_DIR))

from app.config import settings
from generation.chain import RAGChain
from retrieval.retriever import KnowledgeRetriever
from startup_progress import ProgressTicker, show_progress


def main() -> int:
    print()
    print("========================================")
    print("  Preloading Assistant Models")
    print("========================================")
    print()

    show_progress(62, "[4/5] Checking OpenAI API key...")
    if not settings.openai_api_key:
        print()
        print("  [FAIL] OPENAI_API_KEY is missing in .env")
        return 1
    show_progress(68, "[4/5] API key found")

    show_progress(72, "[4/5] Checking document indexes...")
    vector_ready = (settings.vector_store_path / "chroma.sqlite3").exists()
    bm25_ready = (settings.bm25_index_path / "bm25_retriever.pkl").exists()
    if not vector_ready or not bm25_ready:
        print()
        print("  [FAIL] Indexes not found. Run: python scripts\\ingest.py")
        return 1
    show_progress(76, "[4/5] Document indexes found")

    with ProgressTicker(77, 90, "[4/5] Loading ChromaDB, BM25, and reranker..."):
        retriever = KnowledgeRetriever()
    show_progress(92, "[4/5] Retrieval models loaded")

    with ProgressTicker(93, 97, "[4/5] Loading LLM client..."):
        chain = RAGChain()
        chain.attach_shared_retriever(retriever)
        chain.warmup()
    show_progress(98, "[4/5] LLM client ready")

    print()
    print("========================================")
    print("  [OK] All assistant models are ready.")
    print("========================================")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
