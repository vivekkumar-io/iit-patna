"""
Load saved indexes from disk.

After ingestion, two indexes exist:
1. Vector store (ChromaDB) - semantic/meaning search
2. BM25 index - keyword search

Author: Vivek Kumar
"""

import pickle

from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever

from app.config import settings
from ingestion.embedder import get_embedding_model


def load_vector_store() -> Chroma:
    """Load the ChromaDB vector store created during ingestion."""
    settings.vector_store_path.mkdir(parents=True, exist_ok=True)

    return Chroma(
        persist_directory=str(settings.vector_store_path),
        embedding_function=get_embedding_model(),
    )


def load_bm25_retriever() -> BM25Retriever | None:
    """
    Load the BM25 keyword index from disk.

    Returns None if ingestion has not been run yet.
    """
    index_file = settings.bm25_index_path / "bm25_retriever.pkl"

    if not index_file.exists():
        return None

    with open(index_file, "rb") as file:
        bm25_retriever = pickle.load(file)

    bm25_retriever.k = settings.retrieval_top_k
    return bm25_retriever
