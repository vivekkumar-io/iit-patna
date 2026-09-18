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
from app.ui.session import (
    ACADEMIC_DISCLAIMER,
    init_chat_history,
    init_session_state,
    should_show_welcome,
)
from app.ui.sidebar import is_index_ready, render_sidebar
from app.ui.styles import (
    apply_welcome_layout_styles,
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

    init_session_state(settings.show_welcome_page)

    if not is_index_ready():
        if not should_show_welcome(settings.show_welcome_page):
            render_sidebar()
        st.warning("Documents not indexed yet. Run: `python scripts\\ingest.py`")
        st.stop()

    main_area = st.empty()

    if should_show_welcome(settings.show_welcome_page):
        apply_welcome_layout_styles()
        from app.ui.bootstrap import ensure_app_ready
        from app.ui.welcome import render_welcome

        assistant_ready = st.session_state.get("app_ready", False)
        render_welcome(assistant_ready=assistant_ready)

        if not assistant_ready:
            ensure_app_ready()
            st.rerun()

        render_footer_disclaimer(ACADEMIC_DISCLAIMER)
        return

    main_area.empty()

    init_chat_history()
    render_sidebar()

    if not st.session_state.get("app_ready"):
        from app.ui.bootstrap import ensure_app_ready

        ensure_app_ready()

    from app.ui.chat import render_chat

    render_chat()
    render_footer_disclaimer(ACADEMIC_DISCLAIMER)


if __name__ == "__main__":
    main()
