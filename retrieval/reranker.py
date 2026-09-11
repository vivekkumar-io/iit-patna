"""
Reranking step: pick the BEST chunks from many candidates.

Author: Vivek Kumar
"""

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from app.config import settings
from util.logger import get_logger, log_function_end, log_function_start, log_step

logger = get_logger("retrieval.reranker")


class Reranker:
    """Score and sort document chunks by relevance to the user question."""

    def __init__(self):
        log_step(logger, f"Loading reranker model: {settings.reranker_model}")
        self.model = CrossEncoder(settings.reranker_model)

    def rerank(self, user_question: str, documents: list[Document]) -> list[Document]:
        """Return only the most relevant chunks."""
        log_function_start(logger, "Reranker.rerank()")

        if not documents:
            log_function_end(logger, "Reranker.rerank()", "0 chunks")
            return []

        question_document_pairs = [
            (user_question, document.page_content) for document in documents
        ]

        relevance_scores = self.model.predict(question_document_pairs)

        documents_with_scores = list(zip(documents, relevance_scores))
        documents_with_scores.sort(key=lambda item: item[1], reverse=True)

        top_documents = [
            document
            for document, score in documents_with_scores[: settings.rerank_top_n]
        ]

        log_step(
            logger,
            f"Kept top {len(top_documents)} chunks out of {len(documents)}",
        )
        log_function_end(logger, "Reranker.rerank()", f"{len(top_documents)} chunks")
        return top_documents
