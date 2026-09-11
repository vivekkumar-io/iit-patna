"""
Logging utility for the project.

Creates one log file per app run with this name format:
    Enterprise_Knowledge_Assistant_20250907_215930.log

Saved inside the `logs/` folder.

What gets logged:
- Which Python file/function is running
- Step-by-step flow (ingestion, retrieval, answer generation)
- Full prompts sent to the LLM
- LLM responses
- Retrieved document chunks and sources
- Errors

How to use in any Python file:
    from util.logger import get_logger, log_step, log_llm_prompt

    logger = get_logger("generation.chain")
    log_step(logger, "Step 1: Loading documents")

Author: Vivek Kumar
"""

import logging
from datetime import datetime
from pathlib import Path

from app.config import settings

# One log file name for the whole app session (created on first use)
_session_log_file_name: str | None = None


def _build_log_file_name() -> str:
    """
    Build log file name with current date and time.

    Example output:
        Enterprise_Knowledge_Assistant_20250907_215930.log
    """
    now = datetime.now()
    date_time_text = now.strftime("%Y%m%d_%H%M%S")
    return f"Enterprise_Knowledge_Assistant_{date_time_text}.log"


def get_log_file_path() -> Path:
    """
    Return full path of the log file for this session.

    The logs folder is created automatically if it does not exist.
    """
    global _session_log_file_name

    if _session_log_file_name is None:
        settings.logs_path.mkdir(parents=True, exist_ok=True)
        _session_log_file_name = _build_log_file_name()

    return settings.logs_path / _session_log_file_name


def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for one Python module.

    module_name should match the file, for example:
    - "ingestion.loader"
    - "generation.chain"
    - "retrieval.hybrid_retriever"

    This helps you see in the log which Python file wrote each message.
    """
    logger = logging.getLogger(module_name)

    # If logger is already configured, reuse it
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Log format: time | level | module | message
    log_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1) Save logs to file
    file_handler = logging.FileHandler(get_log_file_path(), encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # 2) Also print logs in terminal (useful while learning)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger


def log_step(logger: logging.Logger, step_message: str) -> None:
    """
    Log what step the code is doing right now.

    Example:
        log_step(logger, "Step 2: Splitting documents into chunks")
    """
    logger.info(f"[STEP] {step_message}")


def log_function_start(logger: logging.Logger, function_name: str) -> None:
    """
    Log when a Python function starts.

    Example:
        log_function_start(logger, "run_ingestion()")
    """
    logger.info(f"[PYTHON START] {function_name}")


def log_function_end(
    logger: logging.Logger,
    function_name: str,
    details: str = "",
) -> None:
    """
    Log when a Python function finishes.

    Example:
        log_function_end(logger, "run_ingestion()", "7 documents, 42 chunks")
    """
    if details:
        logger.info(f"[PYTHON END] {function_name} | {details}")
    else:
        logger.info(f"[PYTHON END] {function_name}")


def log_llm_prompt(
    logger: logging.Logger,
    prompt_title: str,
    prompt_text: str,
    system_prompt: str = "",
) -> None:
    """
    Log the full prompt that will be sent to the LLM.

    This is very useful for beginners because you can see
    exactly what text the model receives.
    """
    logger.info("=" * 80)
    logger.info(f"[LLM PROMPT] {prompt_title}")
    logger.info("=" * 80)

    if system_prompt.strip():
        logger.info("[SYSTEM PROMPT]")
        logger.info(system_prompt.strip())
        logger.info("-" * 80)

    logger.info("[USER PROMPT]")
    logger.info(prompt_text.strip())
    logger.info("=" * 80)


def log_llm_response(
    logger: logging.Logger,
    prompt_title: str,
    response_text: str,
) -> None:
    """Log the answer returned by the LLM."""
    logger.info("-" * 80)
    logger.info(f"[LLM RESPONSE] {prompt_title}")
    logger.info(response_text.strip())
    logger.info("-" * 80)


def log_data(logger: logging.Logger, title: str, data: str) -> None:
    """
    Log any useful data (retrieved chunks, sources, counts, etc.).

    Example:
        log_data(logger, "Retrieved Chunks", chunk_text)
    """
    logger.info(f"[DATA] {title}")
    logger.info(data)


def log_error(logger: logging.Logger, error_message: str) -> None:
    """Log an error message."""
    logger.error(f"[ERROR] {error_message}")
