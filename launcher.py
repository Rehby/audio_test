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
    server_address = os.environ.get("STREAMLIT_SERVER_ADDRESS", "127.0.0.1")
    server_port = os.environ.get("STREAMLIT_SERVER_PORT", "8501")
    server_url = f"http://{server_address}:{server_port}"

    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", server_address)
    os.environ.setdefault("STREAMLIT_SERVER_PORT", server_port)

    print(f"Streamlit configured address={server_address} port={server_port}")

    def open_when_ready() -> None:
        # If the server binds to 0.0.0.0, check via localhost for browser access
        host_for_check = "127.0.0.1" if server_address == "0.0.0.0" else server_address

        # First try the configured port
        if wait_for_server(host_for_check, int(server_port), timeout_seconds=10.0):
            url = f"http://{host_for_check}:{server_port}"
            print(f"Opening {url}")
            open_browser(url)
            return

        # If not found, scan common alternative ports Streamlit or other dev servers may use
        common_ports = [3000, 8501, 8080, 8000, 5000, 8502]
        for p in common_ports:
            try:
                if p == int(server_port):
                    continue
            except Exception:
                pass
            if wait_for_server(host_for_check, int(p), timeout_seconds=3.0):
                url = f"http://{host_for_check}:{p}"
                print(f"Detected server on {url}, opening")
                open_browser(url)
                return

        print(f"Server did not start in time. Open http://{host_for_check}:{server_port} manually.")

    threading.Thread(target=open_when_ready, daemon=True).start()

    app_path = get_base_dir() / "app.py"
    bootstrap.run(str(app_path), False, [], {})


if __name__ == "__main__":
    main()