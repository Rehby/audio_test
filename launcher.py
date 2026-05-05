from __future__ import annotations

import os
import socket
import sys
import threading
import time
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


def wait_for_server(host: str, port: int, timeout_seconds: float = 30.0) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def main() -> None:
    server_address = "127.0.0.1"
    server_port = "8501"
    server_url = f"http://{server_address}:{server_port}"

    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", server_address)
    os.environ.setdefault("STREAMLIT_SERVER_PORT", server_port)

    def open_when_ready() -> None:
        if wait_for_server(server_address, int(server_port)):
            print(f"Opening {server_url}")
            open_browser(server_url)
        else:
            print(f"Server did not start in time. Open {server_url} manually.")

    threading.Thread(target=open_when_ready, daemon=True).start()

    app_path = get_base_dir() / "app.py"
    bootstrap.run(str(app_path), False, [], {})


if __name__ == "__main__":
    main()