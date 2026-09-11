"""
Step 1 of ingestion: Load documents from a folder.

Author: Vivek Kumar
"""

from pathlib import Path

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document

from util.logger import get_logger, log_function_end, log_function_start, log_step

logger = get_logger("ingestion.loader")


def load_documents(documents_path: Path) -> list[Document]:
    """Read all supported files from the documents folder."""
    log_function_start(logger, "load_documents()")
    log_step(logger, f"Reading files from: {documents_path}")

    all_documents: list[Document] = []

    if not documents_path.exists():
        log_step(logger, "Documents folder does not exist")
        log_function_end(logger, "load_documents()", "0 documents")
        return all_documents

    for file_path in sorted(documents_path.iterdir()):
        if not file_path.is_file():
            continue

        file_extension = file_path.suffix.lower()

        try:
            if file_extension == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_extension == ".docx":
                loader = Docx2txtLoader(str(file_path))
            elif file_extension == ".txt":
                loader = TextLoader(str(file_path), encoding="utf-8")
            else:
                log_step(logger, f"Skipping unsupported file: {file_path.name}")
                continue

            loaded_docs = loader.load()

            for doc in loaded_docs:
                doc.metadata["source"] = file_path.name

            all_documents.extend(loaded_docs)
            log_step(logger, f"Loaded file: {file_path.name}")

        except Exception as error:
            log_step(logger, f"Failed to load {file_path.name}: {error}")

    log_function_end(
        logger,
        "load_documents()",
        f"{len(all_documents)} document parts loaded",
    )
    return all_documents
