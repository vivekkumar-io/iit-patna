"""
Shared session helpers for the Streamlit UI.

Author: Vivek Kumar
"""

import streamlit as st

ACADEMIC_DISCLAIMER = (
    "* Sample project for academic practice only. "
    "Oeeggis Corporation is fictional and documents are not from a real organization."
)

WELCOME_MESSAGE = (
    "Hello! I am your Enterprise Knowledge Assistant for Oeeggis Corporation "
    "(fictional company for learning purposes). "
    "How can I help you today?"
)

RESET_MESSAGE = (
    "Conversation cleared. Ask me about policies, benefits, travel, IT, or HR FAQs."
)


def get_selected_documents() -> list[str]:
    """Return list of selected document file names from session state."""
    return st.session_state.get("selected_documents", [])


def init_session_state(show_welcome_page: bool) -> None:
    """Initialize UI session flags."""
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = not show_welcome_page


def should_show_welcome(show_welcome_page: bool) -> bool:
    """True when the landing page should appear instead of chat."""
    return show_welcome_page and not st.session_state.get("conversation_started", False)


def init_chat_history() -> None:
    """Create welcome message if chat history is empty."""
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
                "sources": [],
            }
        ]


def reset_chat_history() -> None:
    """Clear chat and reset RAG memory without reloading models."""
    st.session_state.messages = [
        {"role": "assistant", "content": RESET_MESSAGE, "sources": []}
    ]
    st.session_state.pop("pending_question", None)
    if st.session_state.get("rag_chain"):
        st.session_state.rag_chain.reset()
