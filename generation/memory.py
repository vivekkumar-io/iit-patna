"""
LangChain conversation memory (modern API).

Uses InMemoryChatMessageHistory with RunnableWithMessageHistory
and a sliding window of the last N conversation turns.

Author: Vivek Kumar
"""

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.config import settings

SESSION_ID = "enterprise_assistant"


class ChatMemory:
    """Windowed in-memory chat history for multi-turn RAG dialogue."""

    def __init__(self, window_size: int | None = None):
        self.window_size = window_size or settings.memory_window
        self._history = InMemoryChatMessageHistory()

    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """Return message history for RunnableWithMessageHistory (with window trim)."""
        self._trim_window()
        return self._history

    def _trim_window(self) -> None:
        """Keep only the last N user/assistant message pairs."""
        max_messages = self.window_size * 2
        if len(self._history.messages) > max_messages:
            self._history.messages = self._history.messages[-max_messages:]

    @property
    def messages(self) -> list:
        return self._history.messages

    def has_messages(self) -> bool:
        return bool(self._history.messages)

    def format_messages(self) -> str:
        """Format stored messages for RAG prompts."""
        if not self._history.messages:
            return "No prior conversation."

        lines = []
        for message in self._history.messages:
            if isinstance(message, HumanMessage):
                lines.append(f"User: {message.content}")
            elif isinstance(message, AIMessage):
                lines.append(f"Assistant: {message.content}")
        return "\n".join(lines)

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        """Save one completed conversation turn."""
        self._history.add_user_message(user_message)
        self._history.add_ai_message(assistant_message)
        self._trim_window()

    def clear(self) -> None:
        self._history.clear()

    def wrap_with_message_history(self, runnable):
        """Wrap a LangChain runnable with RunnableWithMessageHistory."""
        return RunnableWithMessageHistory(
            runnable,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )


def create_memory() -> ChatMemory:
    """Create windowed chat memory for the RAG assistant."""
    return ChatMemory(window_size=settings.memory_window)
