"""
Main RAG chain (Retrieval-Augmented Generation).

This is the heart of the app.

Full flow when user asks a question:
1. Load LangChain conversation memory (InMemoryChatMessageHistory)
2. Rewrite follow-up questions using RunnableWithMessageHistory
3. Retrieve relevant document chunks (hybrid search + rerank)
4. Build prompt with context + memory
5. Ask LLM to generate answer
6. Save turn to chat memory

Author: Vivek Kumar
"""

import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.config import settings
from generation.guard import (
    format_context_for_llm,
    get_source_list,
    has_documents,
)
from generation.memory import SESSION_ID, create_memory
from generation.prompt import (
    CONTEXT_PROMPT,
    CONVERSATIONAL_PROMPT,
    REWRITE_CHAIN_PROMPT,
    SYSTEM_PROMPT,
)
from retrieval.retriever import KnowledgeRetriever
from util.logger import (
    get_logger,
    log_data,
    log_function_end,
    log_function_start,
    log_llm_prompt,
    log_llm_response,
    log_step,
)

logger = get_logger("generation.chain")

POLICY_KEYWORDS = (
    "policy",
    "leave",
    "travel",
    "benefit",
    "wfh",
    "work from home",
    "sick",
    "insurance",
    "conduct",
    "vpn",
    "reimburse",
    "expense",
    "handbook",
    "faq",
    "holiday",
    "salary",
    "carry",
    "remote",
    "allowance",
    "harassment",
    "metro",
)

MEMORY_QUESTION_PHRASES = (
    "my name",
    "who am i",
    "what did i",
    "what did you",
    "did i tell",
    "did i say",
    "where am i from",
    "which city",
    "remind me",
    "what was my",
)

QUESTION_PHRASES = (
    "what is",
    "what are",
    "what about",
    "how many",
    "how much",
    "how do",
    "how can",
    "can i",
    "could i",
    "do i",
    "does ",
    "is there",
    "tell me",
    "explain",
    "describe",
    "show me",
    "when ",
    "where ",
    "why ",
)


def should_search_documents(user_message: str) -> bool:
    """Return True only when the user is asking for document-based information."""
    normalized = user_message.strip().lower()

    if any(phrase in normalized for phrase in MEMORY_QUESTION_PHRASES):
        return False

    if "?" in user_message:
        return True

    if any(keyword in normalized for keyword in POLICY_KEYWORDS):
        return True

    if any(phrase in normalized for phrase in QUESTION_PHRASES):
        return True

    return False


def _extract_intro_facts(text: str) -> dict[str, str]:
    """Pull name or location from casual intro messages."""
    lower = text.strip().lower()
    facts: dict[str, str] = {}

    name_patterns = (
        r"(?:my name is|call me)\s+([a-z][a-z'-]+)",
        r"(?:i'?m|i am)\s+([a-z][a-z'-]+)(?:\s+and|\s*,|\s+from|$)",
        r"^hi\s+am\s+([a-z][a-z'-]+)",
    )
    for pattern in name_patterns:
        match = re.search(pattern, lower)
        if match:
            facts["name"] = match.group(1).strip().title()
            break

    location_match = re.search(r"from\s+([a-z][a-z\s'-]+)", lower)
    if location_match:
        facts["location"] = location_match.group(1).strip().title()

    return facts


def _message_text(message) -> str:
    content = getattr(message, "content", message)
    if isinstance(content, list):
        return " ".join(str(part) for part in content)
    return str(content)


def build_instant_conversational_reply(
    user_message: str,
    prior_messages: list | None = None,
) -> str:
    """Fast local reply for intros and memory questions — no LLM call."""
    normalized = user_message.strip().lower()
    prior_texts = [_message_text(message) for message in (prior_messages or [])]

    collected_name = None
    collected_location = None
    for text in prior_texts + [user_message]:
        facts = _extract_intro_facts(text)
        collected_name = collected_name or facts.get("name")
        collected_location = collected_location or facts.get("location")

    if any(phrase in normalized for phrase in MEMORY_QUESTION_PHRASES):
        if "name" in normalized or "who am i" in normalized:
            if collected_name:
                return f"You told me your name is {collected_name}."
            return "You have not told me your name yet."

        if "from" in normalized or "city" in normalized:
            if collected_location:
                return f"You mentioned you are from {collected_location}."
            return "You have not told me your location yet."

    facts = _extract_intro_facts(user_message)
    name = facts.get("name")
    location = facts.get("location")

    if name and location:
        return (
            f"Hello {name}! Nice to meet you. I have noted that you are from {location}. "
            "Ask me any question about company policies, benefits, travel, IT, or FAQs."
        )
    if name:
        return (
            f"Hello {name}! Nice to meet you. "
            "Ask me any question about company policies, benefits, travel, IT, or FAQs."
        )
    if location:
        return (
            f"Thanks for sharing! I have noted you are from {location}. "
            "How can I help you with company policies today?"
        )

    return (
        "Thanks for sharing! Ask me any question about company policies, "
        "benefits, travel, IT, or FAQs."
    )


class RAGChain:
    """
    Connects retrieval + LangChain memory + LLM into one simple class.

    Main method to use:
        result = rag_chain.ask("What is the leave policy?")
    """

    def __init__(self):
        log_function_start(logger, "RAGChain.__init__()")
        self._retriever: KnowledgeRetriever | None = None

        log_step(logger, f"Connecting to LLM model: {settings.llm_model}")
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.1,
        )

        log_step(
            logger,
            f"Initializing LangChain memory (window={settings.memory_window})",
        )
        self.chat_memory = create_memory()

        rewrite_prompt = ChatPromptTemplate.from_template(REWRITE_CHAIN_PROMPT)
        rewrite_chain = rewrite_prompt | self.llm | StrOutputParser()
        self.rewrite_chain = self.chat_memory.wrap_with_message_history(rewrite_chain)

        log_function_end(logger, "RAGChain.__init__()", "RAG chain is ready")

    def _get_retriever(self) -> KnowledgeRetriever:
        """Load vector store, BM25, and reranker only when a policy question is asked."""
        if self._retriever is None:
            log_step(logger, "Lazy-loading retriever (vector + BM25 + reranker)")
            self._retriever = KnowledgeRetriever()
        return self._retriever

    def attach_shared_retriever(self, retriever: KnowledgeRetriever) -> None:
        """Reuse a process-wide retriever loaded during app warmup."""
        self._retriever = retriever

    def warmup(self) -> None:
        """Pre-load LLM client and retrieval models at app startup."""
        log_function_start(logger, "RAGChain.warmup()")
        self._get_retriever()
        log_function_end(logger, "RAGChain.warmup()", "All models ready")

    def rewrite_follow_up_question(self, user_question: str) -> str:
        """
        Rewrite follow-up questions using RunnableWithMessageHistory.
        """
        log_function_start(logger, "rewrite_follow_up_question()")

        if not self.chat_memory.has_messages():
            log_step(logger, "No chat history found. Using original question.")
            log_function_end(logger, "rewrite_follow_up_question()", user_question)
            return user_question

        log_step(logger, "Chat history found. Rewriting follow-up question.")
        log_data(logger, "Chat History", self.chat_memory.format_messages())

        messages_before = len(self.chat_memory.messages)
        rewritten_question = self.rewrite_chain.invoke(
            {"input": user_question},
            config={"configurable": {"session_id": SESSION_ID}},
        ).strip()

        # Rewrite invoke auto-saves to history; remove that temporary turn.
        if len(self.chat_memory.messages) > messages_before:
            self.chat_memory.messages[:] = self.chat_memory.messages[:messages_before]

        log_llm_response(
            logger,
            prompt_title="Rewrite Follow-up Question",
            response_text=rewritten_question,
        )
        log_data(
            logger,
            "Question Rewrite",
            f"Original: {user_question}\nRewritten: {rewritten_question}",
        )
        log_function_end(logger, "rewrite_follow_up_question()", rewritten_question)

        return rewritten_question

    def generate_answer_from_context(
        self,
        question: str,
        context: str,
        chat_history: str = "No prior conversation.",
    ) -> str:
        """Send context + history + question to the LLM and return the answer."""
        log_function_start(logger, "generate_answer_from_context()")

        user_prompt = CONTEXT_PROMPT.format(
            context=context,
            question=question,
            chat_history=chat_history,
        )

        log_llm_prompt(
            logger,
            prompt_title="Final Answer Generation",
            prompt_text=user_prompt,
            system_prompt=SYSTEM_PROMPT,
        )

        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", user_prompt),
        ]

        response = self.llm.invoke(messages)
        answer = (response.content or "").strip()
        if isinstance(answer, list):
            answer = " ".join(str(part) for part in answer).strip()
        if not answer:
            answer = "I could not find this information in the available documents."

        log_llm_response(
            logger,
            prompt_title="Final Answer Generation",
            response_text=answer,
        )
        log_function_end(logger, "generate_answer_from_context()", "Answer created")

        return answer

    def generate_conversational_reply(self, question: str) -> str:
        """Reply using chat history only — no document retrieval."""
        log_function_start(logger, "generate_conversational_reply()")

        history_text = self.chat_memory.format_messages()
        user_prompt = CONVERSATIONAL_PROMPT.format(
            chat_history=history_text,
            question=question,
        )

        log_llm_prompt(
            logger,
            prompt_title="Conversational Reply",
            prompt_text=user_prompt,
            system_prompt=SYSTEM_PROMPT,
        )

        response = self.llm.invoke(
            [
                ("system", SYSTEM_PROMPT),
                ("human", user_prompt),
            ]
        )
        answer = (response.content or "").strip()
        if isinstance(answer, list):
            answer = " ".join(str(part) for part in answer).strip()
        if not answer:
            answer = "Thanks for sharing that. How can I help you with company policies?"

        log_llm_response(
            logger,
            prompt_title="Conversational Reply",
            response_text=answer,
        )
        log_function_end(logger, "generate_conversational_reply()", "Reply created")
        return answer

    def _source_filename(self, document: Document) -> str:
        """Get filename from chunk metadata (handles full paths too)."""
        source = document.metadata.get("source", "")
        return Path(source).name if source else ""

    def _filter_by_selected_documents(
        self,
        documents: list[Document],
        selected_documents: list[str] | None,
    ) -> list[Document]:
        """Keep only chunks from documents selected in the sidebar."""
        if not selected_documents:
            return documents

        filtered = [
            document
            for document in documents
            if self._source_filename(document) in selected_documents
        ]
        log_data(
            logger,
            "Filtered By Knowledge Scope",
            f"{len(filtered)} chunks from {len(selected_documents)} selected files",
        )
        return filtered

    def ask(
        self,
        user_question: str,
        selected_documents: list[str] | None = None,
    ) -> dict:
        """
        Main function called by the UI.
        """
        log_function_start(logger, "RAGChain.ask()")
        log_step(logger, f"User asked: {user_question}")

        if not should_search_documents(user_question):
            log_step(logger, "Conversational message detected. Instant reply (no LLM).")
            final_answer = build_instant_conversational_reply(
                user_question,
                prior_messages=self.chat_memory.messages,
            )
            self.chat_memory.add_turn(user_question, final_answer)
            log_function_end(logger, "RAGChain.ask()", "Conversational reply ready")
            return {"answer": final_answer, "sources": []}

        history_text = self.chat_memory.format_messages()

        # STEP 1: Handle follow-up questions using LangChain memory
        log_step(logger, "STEP 1: Rewrite question using chat memory")
        search_question = self.rewrite_follow_up_question(user_question)

        # STEP 2: Retrieve relevant chunks
        log_step(logger, "STEP 2: Retrieve relevant document chunks")
        relevant_documents = self._get_retriever().retrieve(
            search_question,
            selected_documents=selected_documents,
        )
        relevant_documents = self._filter_by_selected_documents(
            relevant_documents,
            selected_documents,
        )

        log_data(
            logger,
            "Retrieved Chunk Count",
            str(len(relevant_documents)),
        )

        # STEP 3: If nothing found, try conversation history before giving up
        if not has_documents(relevant_documents):
            if self.chat_memory.has_messages():
                log_step(logger, "STEP 3: No documents found. Trying chat history.")
                final_answer = self.generate_answer_from_context(
                    user_question,
                    "No relevant document context found.",
                    chat_history=history_text,
                )
                self.chat_memory.add_turn(user_question, final_answer)
                log_function_end(logger, "RAGChain.ask()", "Answer ready from history")
                return {"answer": final_answer, "sources": []}

            log_step(logger, "STEP 3: No documents found. Returning safe message.")
            safe_answer = "I could not find this information in the available documents."
            self.chat_memory.add_turn(user_question, safe_answer)
            log_function_end(logger, "RAGChain.ask()", "No context found")
            return {"answer": safe_answer, "sources": []}

        # STEP 4: Build context text for the LLM
        log_step(logger, "STEP 4: Build context text for LLM")
        context_text = format_context_for_llm(relevant_documents)
        log_data(logger, "Context Sent To LLM", context_text)

        # STEP 5: Generate final answer
        log_step(logger, "STEP 5: Ask LLM to generate final answer")
        final_answer = self.generate_answer_from_context(
            user_question,
            context_text,
            chat_history=history_text,
        )

        # STEP 6: Collect source file names
        log_step(logger, "STEP 6: Collect source citations")
        source_files = get_source_list(relevant_documents)
        log_data(logger, "Sources", ", ".join(source_files))

        # STEP 7: Save this turn in LangChain memory
        log_step(logger, "STEP 7: Save conversation in LangChain memory")
        self.chat_memory.add_turn(user_question, final_answer)

        log_function_end(logger, "RAGChain.ask()", "Answer ready")
        return {
            "answer": final_answer,
            "sources": source_files,
        }

    def reset(self) -> None:
        """Clear LangChain conversation memory."""
        log_step(logger, "LangChain conversation memory cleared")
        self.chat_memory.clear()
