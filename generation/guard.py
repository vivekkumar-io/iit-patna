"""
Helper functions to prepare context and sources for the LLM.

Also includes a simple check to avoid answering when no context is found.

Author: Vivek Kumar
"""

from pathlib import Path

from langchain_core.documents import Document


def format_context_for_llm(documents: list[Document]) -> str:
    """
    Convert retrieved chunks into one text block for the LLM prompt.

    Each chunk is labeled with its source file name.
    """
    if not documents:
        return "No relevant context found."

    context_parts = []

    for document in documents:
        source_name = document.metadata.get("source", "Unknown")
        page_number = document.metadata.get("page", "")

        # PDF pages are often stored as 0, 1, 2... so we show page + 1
        if isinstance(page_number, int):
            source_label = f"{source_name} (page {page_number + 1})"
        else:
            source_label = source_name

        chunk_text = f"[{source_label}]\n{document.page_content}"
        context_parts.append(chunk_text)

    return "\n\n---\n\n".join(context_parts)


def get_source_list(documents: list[Document]) -> list[str]:
    """
    Build a clean list of source files for the UI.

    Example output:
    ["Leave_Policy.txt", "HR_Handbook.txt (page 2)"]
    """
    source_list = []
    already_added = set()

    for document in documents:
        source_path = document.metadata.get("source", "Unknown")
        source_name = Path(source_path).name if source_path else "Unknown"
        page_number = document.metadata.get("page", "")

        if isinstance(page_number, int):
            source_label = f"{source_name} (page {page_number + 1})"
        else:
            source_label = source_name

        if source_label not in already_added:
            already_added.add(source_label)
            source_list.append(source_label)

    return source_list


def has_documents(documents: list[Document]) -> bool:
    """Return True if we found at least one relevant chunk."""
    return len(documents) > 0
