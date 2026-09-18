"""
Check whether document indexes exist on disk.

Author: Vivek Kumar
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import settings

INDEX_FLAG = settings.documents_path.parent / ".index_ready"


def indexes_exist() -> bool:
    chroma_ready = (settings.vector_store_path / "chroma.sqlite3").exists()
    bm25_ready = (settings.bm25_index_path / "bm25_retriever.pkl").exists()
    return chroma_ready and bm25_ready


def mark_index_ready() -> None:
    INDEX_FLAG.write_text("Document indexes built successfully.\n", encoding="utf-8")


def main() -> int:
    if "--mark-ready" in sys.argv:
        if indexes_exist():
            mark_index_ready()
            print("Index flag created.")
            return 0
        print("Cannot mark ready: indexes are missing.")
        return 1

    if indexes_exist():
        print("Indexes ready: ChromaDB + BM25 found.")
        return 0

    print("Indexes missing. Run setup.bat once, or reindex.bat after adding documents.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
