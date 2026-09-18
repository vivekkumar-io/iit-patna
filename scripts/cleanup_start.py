"""
Fast startup cleanup for start.bat.

- Stops any process listening on port 8501
- Clears project __pycache__ folders (skips venv and data)

Author: Vivek Kumar
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from startup_progress import show_progress

SOURCE_DIRS = ("app", "ingestion", "retrieval", "generation", "util", "scripts")
SKIP_DIR_NAMES = {"venv", ".git", "data", "logs", "node_modules"}


def kill_listeners_on_port(port: int) -> int:
    """Stop Windows processes listening on the given TCP port."""
    result = subprocess.run(
        ["netstat", "-ano"],
        capture_output=True,
        text=True,
        check=False,
    )
    pids: set[str] = set()
    needle = f":{port}"
    for line in result.stdout.splitlines():
        if needle not in line or "LISTENING" not in line:
            continue
        parts = line.split()
        if parts and parts[-1].isdigit():
            pids.add(parts[-1])

    stopped = 0
    for pid in pids:
        stop = subprocess.run(
            ["taskkill", "/F", "/PID", pid],
            capture_output=True,
            text=True,
            check=False,
        )
        if stop.returncode == 0:
            stopped += 1
    return stopped


def clear_project_pycache() -> int:
    """Remove __pycache__ only from project source folders."""
    removed = 0
    for folder_name in SOURCE_DIRS:
        base = PROJECT_ROOT / folder_name
        if not base.exists():
            continue
        for cache_dir in base.rglob("__pycache__"):
            if any(part in SKIP_DIR_NAMES for part in cache_dir.parts):
                continue
            if cache_dir.is_dir():
                shutil.rmtree(cache_dir, ignore_errors=True)
                removed += 1
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Startup cleanup helper")
    parser.add_argument("--port", type=int, default=8501)
    parser.add_argument("--kill-port", action="store_true")
    parser.add_argument("--clear-cache", action="store_true")
    args = parser.parse_args()

    if args.kill_port:
        show_progress(5, "[1/5] Stopping old Streamlit on port 8501...")
        kill_listeners_on_port(args.port)
        show_progress(20, "[1/5] Port 8501 ready")

    if args.clear_cache:
        show_progress(25, "[2/5] Clearing Python __pycache__ folders...")
        clear_project_pycache()
        show_progress(40, "[2/5] Cache folders cleared")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
