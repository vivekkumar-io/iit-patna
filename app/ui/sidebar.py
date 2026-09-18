"""
Sidebar - wireframe layout only.

Author: Vivek Kumar
"""

import streamlit as st

from app.config import settings
from app.ui.session import ACADEMIC_DISCLAIMER, reset_chat_history

TOPIC_LABELS = {
    "Benefits_Documentation": "Benefits & Perks",
    "Code_of_Conduct": "Code of Conduct",
    "Company_FAQs": "Company FAQs",
    "HR_Handbook": "HR Handbook",
    "IT_Policy": "IT & Security Policy",
    "Leave_Policy": "Leave Policy",
    "Travel_Policy": "Travel Policy",
}


def is_index_ready() -> bool:
    vector_exists = (settings.vector_store_path / "chroma.sqlite3").exists()
    bm25_exists = (settings.bm25_index_path / "bm25_retriever.pkl").exists()
    return vector_exists and bm25_exists


def _topic_label(filename_stem: str) -> str:
    if filename_stem in TOPIC_LABELS:
        return TOPIC_LABELS[filename_stem]
    return filename_stem.replace("_", " ").strip()


def _list_documents() -> list[tuple[str, str]]:
    if not settings.documents_path.exists():
        return []

    docs = []
    for file_path in sorted(settings.documents_path.iterdir()):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".txt", ".pdf", ".docx"}:
            continue
        docs.append((file_path.name, _topic_label(file_path.stem)))
    return docs


def render_sidebar() -> None:
    """Blue sidebar: knowledge scope list + Clear/Reset button."""
    documents = _list_documents()
    all_filenames = [name for name, _ in documents]
    st.session_state.selected_documents = all_filenames

    with st.sidebar:
        st.markdown("## Knowledge Base")
        st.caption("Company policies and employee guides")
        st.markdown("---")

        if documents:
            bullet_items = "".join(
                f"<li>{topic}</li>" for _, topic in documents
            )
            st.markdown(
                f'<ul class="knowledge-scope-list">{bullet_items}</ul>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<p class="knowledge-scope-empty">No documents found.</p>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.button("Clear / Reset", on_click=reset_chat_history, use_container_width=True)
        st.markdown("---")
        st.caption(ACADEMIC_DISCLAIMER)
