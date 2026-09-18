"""
CLI script to ingest documents.

Author: Vivek Kumar
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.pipeline import run_ingestion
from util.logger import get_logger, log_data, log_step

logger = get_logger("scripts.ingest")


def main() -> None:
    log_step(logger, "Ingestion script started from command line")
    print("Starting document ingestion...")
    print("This may take a few minutes on first run.\n")

    result = run_ingestion()

    if result["status"] == "success":
        log_data(
            logger,
            "Ingestion Result",
            f"Documents: {result['document_count']}, Chunks: {result['chunk_count']}",
        )
        print("SUCCESS!")
        print(f"Documents loaded: {result['document_count']}")
        print(f"Chunks created:   {result['chunk_count']}")

        from scripts.check_index import mark_index_ready

        mark_index_ready()
        print("\nIndexes saved. You can now run start.bat.")
    else:
        log_step(logger, f"Ingestion failed: {result['message']}")
        print("FAILED!")
        print(result["message"])
        sys.exit(1)


if __name__ == "__main__":
    main()
