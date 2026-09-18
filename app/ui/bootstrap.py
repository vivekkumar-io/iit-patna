"""
Startup helpers — preload all models once when the app opens.

Author: Vivek Kumar
"""

import streamlit as st


@st.cache_resource(show_spinner=False)
def get_shared_retriever():
    """Load ChromaDB, BM25, and reranker once per Streamlit server process."""
    from retrieval.retriever import KnowledgeRetriever

    return KnowledgeRetriever()


def get_rag_chain():
    """Return the session RAG chain, wired to the shared retriever."""
    if st.session_state.get("rag_chain") is None:
        from generation.chain import RAGChain

        chain = RAGChain()
        chain.attach_shared_retriever(get_shared_retriever())
        st.session_state.rag_chain = chain
    return st.session_state.rag_chain


def ensure_app_ready() -> None:
    """Load every component at startup before the user can chat."""
    if st.session_state.get("app_ready"):
        return

    retriever = get_shared_retriever()
    chain = get_rag_chain()
    chain.attach_shared_retriever(retriever)
    chain.warmup()

    st.session_state.app_ready = True
    st.session_state.rag_warmup_done = True
