"""
Chat area - lightweight, wireframe layout.

Author: Vivek Kumar
"""

import time

import streamlit as st

from app.ui.bootstrap import get_rag_chain
from app.ui.session import get_selected_documents
from generation.chain import build_instant_conversational_reply, should_search_documents

GREETING_REPLY = (
    "Hello! I am your Enterprise Knowledge Assistant for Oeeggis Corporation "
    "(fictional company for learning purposes). "
    "Ask me any question about company policies, benefits, travel, IT, or FAQs."
)

MIN_REPLY_SECONDS = 2.0


def show_sources(sources: list[str]) -> None:
    """Display retrieved document sources under an assistant answer."""
    if not sources:
        return

    items = "".join(f"<li>{source}</li>" for source in sources)
    st.markdown(
        f'<div class="source-citations"><strong>Sources:</strong><ul>{items}</ul></div>',
        unsafe_allow_html=True,
    )


def show_thinking_indicator() -> None:
    """Show typing dots in the assistant answer area."""
    st.markdown(
        """
        <div class="thinking-row">
            <div class="thinking-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _repair_orphan_messages() -> None:
    """Fix only real interrupted chats (e.g. browser refresh), not active replies."""
    if st.session_state.get("pending_question"):
        return

    messages = st.session_state.messages
    if messages and messages[-1].get("thinking"):
        return

    if messages and messages[-1]["role"] == "user":
        messages.append(
            {
                "role": "assistant",
                "content": "The previous request was interrupted. Please ask your question again.",
                "sources": [],
            }
        )


def _is_greeting(text: str) -> bool:
    words = text.strip().lower().split()
    return len(words) <= 3 and words[0] in {"hi", "hello", "hey", "hii", "hola"}


def _get_answer(question: str) -> dict:
    if _is_greeting(question):
        rag_chain = get_rag_chain()
        rag_chain.chat_memory.add_turn(question, GREETING_REPLY)
        return {"answer": GREETING_REPLY, "sources": []}

    if not should_search_documents(question):
        rag_chain = get_rag_chain()
        reply = build_instant_conversational_reply(
            question,
            prior_messages=rag_chain.chat_memory.messages,
        )
        rag_chain.chat_memory.add_turn(question, reply)
        return {"answer": reply, "sources": []}

    selected = get_selected_documents()
    rag_chain = get_rag_chain()
    result = rag_chain.ask(question, selected_documents=selected or None)
    answer = (result.get("answer") or "").strip()
    if not answer:
        answer = "I could not find this information in the available documents."

    return {"answer": answer, "sources": result.get("sources", [])}


def _process_pending_question(question: str) -> dict:
    """Brief thinking pause for policy questions; intros reply faster."""
    if should_search_documents(question):
        time.sleep(MIN_REPLY_SECONDS)

    try:
        return _get_answer(question)
    except Exception as e:
        return {"answer": f"An error occurred: {e}", "sources": []}


def render_chat() -> None:
    """Render chat history and handle new user input."""
    _repair_orphan_messages()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("thinking"):
                show_thinking_indicator()
            else:
                content = msg.get("content") or ""
                st.markdown(content if content else "_No response generated._")
                if msg["role"] == "assistant":
                    show_sources(msg.get("sources") or [])

    question = st.chat_input("Ask a question...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question, "sources": []})
        st.session_state.messages.append(
            {"role": "assistant", "content": "", "sources": [], "thinking": True}
        )
        st.session_state.pending_question = question
        st.rerun()

    pending = st.session_state.get("pending_question")
    if pending:
        result = _process_pending_question(pending)

        st.session_state.messages[-1] = {
            "role": "assistant",
            "content": result["answer"],
            "sources": result.get("sources", []),
        }
        del st.session_state.pending_question
        st.rerun()
