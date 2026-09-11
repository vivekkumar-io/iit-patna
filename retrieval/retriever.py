"""
Main retrieval class used by the chat app.

This file connects:
- Vector store
- BM25 index
- Hybrid retriever
- Reranker

Author: Vivek Kumar
"""

from app.config import settings
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker
from retrieval.vector_store import load_bm25_retriever, load_vector_store
from util.logger import get_logger, log_function_end, log_function_start, log_step

logger = get_logger("retrieval.retriever")


class KnowledgeRetriever:
    """
    Simple interface: give a question, get relevant document chunks.

    Usage:
        retriever = KnowledgeRetriever()
        chunks = retriever.retrieve("What is the leave policy?")
    """

    def __init__(self):
        log_function_start(logger, "KnowledgeRetriever.__init__()")

        log_step(logger, "Loading vector store from disk")
        self.vector_store = load_vector_store()

        log_step(logger, "Loading BM25 index from disk")
        self.bm25_retriever = load_bm25_retriever()
        self.reranker = Reranker()

        if self.bm25_retriever is None:
            raise FileNotFoundError(
                "BM25 index not found. Please run ingestion first:\n"
                "python scripts/ingest.py"
            )

        # Vector retriever searches by meaning
        self.vector_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": settings.retrieval_top_k}
        )

        # Hybrid retriever combines vector + keyword + reranking
        self.hybrid_retriever = HybridRetriever(
            vector_retriever=self.vector_retriever,
            bm25_retriever=self.bm25_retriever,
            reranker=self.reranker,
        )
        log_function_end(logger, "KnowledgeRetriever.__init__()", "Retriever ready")

    def retrieve(self, user_question: str, selected_documents: list[str] | None = None):
        """Find the most relevant chunks for a user question."""
        return self.hybrid_retriever.retrieve(
            user_question,
            selected_documents=selected_documents,
        )
