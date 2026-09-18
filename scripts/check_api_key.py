"""
Verify OPENAI_API_KEY is set in .env.

Author: Vivek Kumar
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import settings


def main() -> int:
    if settings.openai_api_key.strip():
        print("OPENAI_API_KEY is set.")
        return 0

    print("OPENAI_API_KEY is missing in .env")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
