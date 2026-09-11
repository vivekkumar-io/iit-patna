"""
Step 2 of ingestion: Split large documents into smaller chunks.

Author: Vivek Kumar
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from util.logger import get_logger, log_function_end, log_function_start, log_step

logger = get_logger("ingestion.chunker")


def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split documents into smaller text chunks."""
    log_function_start(logger, "chunk_documents()")
    log_step(
        logger,
        f"Chunk size={settings.chunk_size}, overlap={settings.chunk_overlap}",
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    log_function_end(
        logger,
        "chunk_documents()",
        f"{len(chunks)} chunks created",
    )
    return chunks
