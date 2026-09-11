"""
Main ingestion pipeline.

Author: Vivek Kumar
"""

import pickle
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

from app.config import settings
from ingestion.chunker import chunk_documents
from ingestion.embedder import get_embedding_model
from ingestion.loader import load_documents
from util.logger import (
    get_logger,
    log_function_end,
    log_function_start,
    log_step,
)

logger = get_logger("ingestion.pipeline")


def save_bm25_index(bm25_retriever: BM25Retriever, save_path: Path) -> None:
    """Save BM25 index to disk."""
    log_function_start(logger, "save_bm25_index()")

    save_path.mkdir(parents=True, exist_ok=True)
    index_file = save_path / "bm25_retriever.pkl"

    with open(index_file, "wb") as file:
        pickle.dump(bm25_retriever, file)

    log_step(logger, f"BM25 index saved to: {index_file}")
    log_function_end(logger, "save_bm25_index()")


def save_vector_store(chunks: list[Document]) -> Chroma:
    """Save document chunks and embeddings in ChromaDB."""
    log_function_start(logger, "save_vector_store()")

    settings.vector_store_path.mkdir(parents=True, exist_ok=True)
    embedding_model = get_embedding_model()

    log_step(logger, "Creating embeddings and saving to ChromaDB")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(settings.vector_store_path),
    )

    log_step(logger, f"Vector store saved to: {settings.vector_store_path}")
    log_function_end(logger, "save_vector_store()")
    return vector_store


def run_ingestion(documents_path: Path | None = None) -> dict:
    """Run the complete ingestion process."""
    log_function_start(logger, "run_ingestion()")

    folder_path = documents_path or settings.documents_path
    print("\n=== Starting Document Ingestion ===\n")

    # STEP 1
    log_step(logger, "STEP 1: Load documents from folder")
    print("Step 1: Loading documents...")
    documents = load_documents(folder_path)

    if not documents:
        log_step(logger, "No documents found")
        log_function_end(logger, "run_ingestion()", "Failed - no documents")
        return {
            "status": "error",
            "message": (
                f"No documents found in {folder_path}. "
                "Please add PDF, DOCX, or TXT files."
            ),
            "document_count": 0,
            "chunk_count": 0,
        }

    # STEP 2
    log_step(logger, "STEP 2: Split documents into chunks")
    print("\nStep 2: Splitting into chunks...")
    chunks = chunk_documents(documents)

    # STEP 3
    log_step(logger, "STEP 3: Build vector store")
    print("\nStep 3: Building vector store...")
    save_vector_store(chunks)

    # STEP 4
    log_step(logger, "STEP 4: Build BM25 keyword index")
    print("\nStep 4: Building BM25 index...")
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = settings.retrieval_top_k
    save_bm25_index(bm25_retriever, settings.bm25_index_path)

    print("\n=== Ingestion Completed Successfully ===\n")
    log_function_end(
        logger,
        "run_ingestion()",
        f"{len(documents)} docs, {len(chunks)} chunks",
    )

    return {
        "status": "success",
        "message": "Ingestion completed successfully.",
        "document_count": len(documents),
        "chunk_count": len(chunks),
    }
