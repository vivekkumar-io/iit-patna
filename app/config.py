"""
Configuration file for the project.

This file stores all important settings in one place:
- API keys (from .env file)
- File paths
- Chunk size, retrieval settings, etc.

Beginners: Change values here instead of searching through many files.

Author: Vivek Kumar
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root folder (Enterprise_Knowledge_Assistant/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    All app settings.

    Values can come from:
    1. Default values below
    2. .env file (example: OPENAI_API_KEY=sk-...)
    """

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- OpenAI settings ---
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"  # Chat model for answers
    embedding_model: str = "text-embedding-3-small"  # Model to create vectors
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # Reranking model

    # --- Folder paths ---
    documents_path: Path = PROJECT_ROOT / "data" / "documents"
    vector_store_path: Path = PROJECT_ROOT / "data" / "vector_store"
    bm25_index_path: Path = PROJECT_ROOT / "data" / "bm25_index"
    logs_path: Path = PROJECT_ROOT / "logs"

    # --- Chunking settings ---
    # Large documents are split into small pieces (chunks) for better search
    chunk_size: int = 600  # Characters per chunk
    chunk_overlap: int = 120  # Overlap helps keep context between chunks

    # --- Retrieval settings ---
    retrieval_top_k: int = 15  # How many chunks to fetch before reranking
    rerank_top_n: int = 5  # How many best chunks to send to the LLM
    memory_window: int = 5  # How many past chat turns to remember


# Create one settings object used across the whole app
settings = Settings()
