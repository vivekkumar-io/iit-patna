"""
Step 3 of ingestion: Create embeddings (vector representations of text).

What is an embedding?
- A list of numbers that represents the meaning of text
- Similar meanings -> similar vectors
- Used for semantic (meaning-based) search

Author: Vivek Kumar
"""

from langchain_openai import OpenAIEmbeddings

from app.config import settings


def get_embedding_model() -> OpenAIEmbeddings:
    """
    Return the OpenAI embedding model.

    This model converts text into vectors for the vector database.
    """
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
