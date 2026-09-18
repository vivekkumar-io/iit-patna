"""
Welcome landing page — shown before the chat interface.

Author: Vivek Kumar
"""

import streamlit as st

from app.ui.session import init_chat_history


def _start_conversation() -> None:
    st.session_state.conversation_started = True
    init_chat_history()


def _html_line(markup: str) -> None:
    """Render one small HTML snippet (Streamlit escapes large/multi-tag blocks)."""
    st.markdown(markup, unsafe_allow_html=True)


def render_welcome(assistant_ready: bool = True) -> None:
    """Landing page with project intro and Start Conversation button."""
    _html_line('<p class="welcome-badge">IIT Patna · GenAI Development Program</p>')
    _html_line('<p class="welcome-title">Enterprise Knowledge Assistant</p>')
    _html_line(
        '<p class="welcome-subtitle">Oeeggis Corporation — AI-powered policy and employee guide</p>'
    )

    _html_line('<p class="welcome-h">About this project</p>')
    _html_line(
        '<p class="welcome-body">Employees often search through long HR, IT, travel, and '
        "benefits documents to find simple answers. This assistant lets them ask questions "
        "in natural language and receive grounded responses from company policy documents.</p>"
    )

    _html_line('<p class="welcome-h">Key benefits</p>')
    for benefit in (
        "Save time — no need to search through long policy documents",
        "Ask questions in simple, everyday language",
        "Get clear answers based on official company policies",
        "Continue the conversation with follow-up questions",
        "One place for HR, travel, leave, benefits, and IT help",
    ):
        _html_line(f'<p class="welcome-body welcome-bullet">• {benefit}</p>')

    _html_line('<p class="welcome-h welcome-h-builtby">Built by</p>')
    _html_line('<p class="welcome-name">Vivek Kumar</p>')
    _html_line(
        '<p class="welcome-note">Click below to open the live assistant and start your conversation.</p>'
    )

    if not assistant_ready:
        _html_line('<p class="welcome-loading">Loading assistant models...</p>')

    st.button(
        "Start Conversation" if assistant_ready else "Please wait...",
        on_click=_start_conversation,
        type="primary",
        use_container_width=True,
        key="start_conversation_btn",
        disabled=not assistant_ready,
    )
