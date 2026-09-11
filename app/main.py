"""
Streamlit entry point - lightweight UI with wireframe layout.

Author: Vivek Kumar
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import settings
from app.ui.bootstrap import ensure_app_ready
from app.ui.chat import render_chat
from app.ui.session import ACADEMIC_DISCLAIMER, init_chat_history
from app.ui.sidebar import is_index_ready, render_sidebar
from app.ui.styles import (
    apply_wireframe_styles,
    render_footer_disclaimer,
    render_header_banner,
)


def main() -> None:
    st.set_page_config(
        page_title="Oeeggis Corporation - Enterprise Knowledge Assistant",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_wireframe_styles()
    render_header_banner()

    if not settings.openai_api_key:
        st.error("OpenAI API key missing. Add OPENAI_API_KEY to your .env file.")
        st.stop()

    init_chat_history()

    if not is_index_ready():
        render_sidebar()
        st.warning("Documents not indexed yet. Run: `python scripts\\ingest.py`")
        st.stop()

    if not st.session_state.get("app_ready"):
        with st.spinner("Loading assistant models... First start may take 1-2 minutes. Please wait."):
            ensure_app_ready()
    else:
        ensure_app_ready()

    render_sidebar()
    render_chat()
    render_footer_disclaimer(ACADEMIC_DISCLAIMER)


if __name__ == "__main__":
    main()
