from __future__ import annotations

import os
import sys
import threading
import webbrowser
from pathlib import Path

from streamlit.web import bootstrap


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def open_browser(url: str) -> None:
    try:
        webbrowser.open(url)
    except Exception:
        pass


def main() -> None:
    server_address = "127.0.0.1"
    server_port = "8501"
    server_url = f"http://{server_address}:{server_port}"

    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", server_address)
    os.environ.setdefault("STREAMLIT_SERVER_PORT", server_port)

    print(f"Opening {server_url}")
    threading.Timer(2.0, open_browser, args=(server_url,)).start()

    app_path = get_base_dir() / "app.py"
    bootstrap.run(str(app_path), False, [], {})


if __name__ == "__main__":
    main()