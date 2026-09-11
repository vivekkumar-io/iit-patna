"""
Hybrid search = Vector search + Keyword search (BM25).

Author: Vivek Kumar
"""

from pathlib import Path

from langchain_core.documents import Document

from retrieval.reranker import Reranker
from util.logger import get_logger, log_function_end, log_function_start, log_step

logger = get_logger("retrieval.hybrid_retriever")


def combine_search_results(
    vector_results: list[Document],
    keyword_results: list[Document],
    k: int = 60,
) -> list[Document]:
    """Merge vector and keyword results using Reciprocal Rank Fusion (RRF)."""
    log_function_start(logger, "combine_search_results()")

    final_scores: dict[str, float] = {}
    document_by_text: dict[str, Document] = {}

    for rank, document in enumerate(vector_results):
        text_key = document.page_content
        score_boost = 1.0 / (k + rank + 1)
        final_scores[text_key] = final_scores.get(text_key, 0.0) + score_boost
        document_by_text[text_key] = document

    for rank, document in enumerate(keyword_results):
        text_key = document.page_content
        score_boost = 1.0 / (k + rank + 1)
        final_scores[text_key] = final_scores.get(text_key, 0.0) + score_boost
        document_by_text[text_key] = document

    sorted_text_keys = sorted(
        final_scores.keys(),
        key=lambda text_key: final_scores[text_key],
        reverse=True,
    )

    combined = [document_by_text[text_key] for text_key in sorted_text_keys]
    log_function_end(
        logger,
        "combine_search_results()",
        f"{len(combined)} unique chunks after merge",
    )
    return combined


def _filter_by_sources(
    documents: list[Document],
    selected_sources: list[str] | None,
) -> list[Document]:
    if not selected_sources:
        return documents

    return [
        document
        for document in documents
        if Path(document.metadata.get("source", "")).name in selected_sources
    ]


class HybridRetriever:
    """Run vector + keyword search, merge results, then rerank."""

    def __init__(self, vector_retriever, bm25_retriever, reranker: Reranker):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        self.reranker = reranker

    def retrieve(
        self,
        user_question: str,
        selected_documents: list[str] | None = None,
    ) -> list[Document]:
        """Full retrieval pipeline for one question."""
        log_function_start(logger, "HybridRetriever.retrieve()")
        log_step(logger, f"Searching for: {user_question}")

        log_step(logger, "Sub-step 1: Vector (semantic) search")
        vector_results = self.vector_retriever.invoke(user_question)
        log_step(logger, f"Vector search returned {len(vector_results)} chunks")

        log_step(logger, "Sub-step 2: BM25 (keyword) search")
        keyword_results = self.bm25_retriever.invoke(user_question)
        log_step(logger, f"BM25 search returned {len(keyword_results)} chunks")

        log_step(logger, "Sub-step 3: Combine both result lists")
        combined_results = combine_search_results(vector_results, keyword_results)
        combined_results = _filter_by_sources(combined_results, selected_documents)

        log_step(logger, "Sub-step 4: Rerank and keep best chunks")
        best_chunks = self.reranker.rerank(user_question, combined_results)
        log_function_end(
            logger,
            "HybridRetriever.retrieve()",
            f"{len(best_chunks)} final chunks",
        )

        return best_chunks
