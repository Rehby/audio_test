from __future__ import annotations

import os
import sys
from pathlib import Path

from streamlit.web import bootstrap


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def main() -> None:
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "false")
    app_path = get_base_dir() / "app.py"
    bootstrap.run(str(app_path), False, [], {})


if __name__ == "__main__":
    main()