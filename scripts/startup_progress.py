"""
Console progress bar helpers for start.bat and warmup.py.

Author: Vivek Kumar
"""

import os
import sys
import threading
import time

_ANSI_ENABLED = False
_USE_ASCII_BAR = False


def _configure_stdout() -> None:
    """Prefer UTF-8 on Windows consoles; fall back to ASCII progress bars."""
    global _USE_ASCII_BAR
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            return
        except Exception:
            pass
    encoding = getattr(sys.stdout, "encoding", None) or ""
    if encoding.lower() not in {"utf-8", "utf8"}:
        _USE_ASCII_BAR = True


def _enable_ansi() -> None:
    global _ANSI_ENABLED
    if _ANSI_ENABLED:
        return
    if sys.platform == "win32":
        os.system("")
    _ANSI_ENABLED = True


def show_progress(percent: int, message: str) -> None:
    """Render a single-line percentage status bar in the terminal."""
    _configure_stdout()
    _enable_ansi()
    percent = max(0, min(100, percent))
    width = 40
    filled = int(width * percent / 100)
    empty = width - filled
    if _USE_ASCII_BAR:
        filled_bar = "#" * filled
        empty_bar = "-" * empty
        line = f"[{filled_bar}{empty_bar}] {percent:3d}%  {message}"
    else:
        # Solid white filled bar; dim blocks for remaining portion
        filled_bar = "\033[97m" + "\u2588" * filled + "\033[0m"
        empty_bar = "\033[90m" + "\u2591" * empty + "\033[0m"
        bar = filled_bar + empty_bar
        line = f"[{bar}] \033[97m{percent:3d}%\033[0m  {message}"
    try:
        sys.stdout.write("\r" + line.ljust(110))
        sys.stdout.flush()
    except UnicodeEncodeError:
        ascii_line = (
            f"[{'#' * filled}{'-' * empty}] {percent:3d}%  "
            f"{message.encode('ascii', 'replace').decode('ascii')}"
        )
        sys.stdout.write("\r" + ascii_line.ljust(110))
        sys.stdout.flush()
    if percent >= 100:
        sys.stdout.write("\n")


class ProgressTicker:
    """Animate progress while a long blocking task runs."""

    def __init__(self, start: int, end: int, message: str, interval: float = 0.4):
        self.start = start
        self.end = end
        self.message = message
        self.interval = interval
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._current = start

    def __enter__(self):
        def _run() -> None:
            while not self._stop.is_set() and self._current < self.end:
                show_progress(self._current, self.message)
                time.sleep(self.interval)
                self._current += 1

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1)
        show_progress(self.end, self.message)


def main() -> None:
    """CLI: python scripts/startup_progress.py <percent> <message>"""
    if len(sys.argv) < 3:
        print("Usage: python scripts/startup_progress.py <percent> <message>")
        raise SystemExit(1)
    show_progress(int(sys.argv[1]), " ".join(sys.argv[2:]))


if __name__ == "__main__":
    main()
