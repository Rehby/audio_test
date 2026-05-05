import subprocess
import sys
import time
import webbrowser
import socket
import threading
from pathlib import Path


def wait_for_port(host: str, port: int, timeout: int = 30) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            time.sleep(0.5)
    return False


def stream_reader(pipe, buffer: list):
    try:
        for line in iter(pipe.readline, ""):
            print(line, end="")
            buffer.append(line)
    finally:
        pipe.close()


def main() -> int:
    # Determine base path: if frozen by PyInstaller, files are extracted to sys._MEIPASS
    if getattr(sys, "frozen", False):
        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    else:
        base_path = Path(__file__).parent

    app_path = base_path / "app.py"
    if not app_path.exists():
        print(f"Error: app.py not found at {app_path!s}")
        return 2

    # Prefer running Streamlit programmatically when possible (works inside a PyInstaller bundle)
    host = "127.0.0.1"
    port = 3000

    try:
        # Try the newer import path first
        try:
            from streamlit.web import cli as stcli
        except Exception:
            # Fallback for older Streamlit versions
            import streamlit.cli as stcli

        # Replace sys.argv similar to running `streamlit run app.py ...`
        sys_argv_backup = sys.argv[:]
        # Disable CORS and XSRF protection to avoid cross-origin restrictions when desired
        sys.argv = [
            "streamlit",
            "run",
            str(app_path),
            "--server.headless",
            "true",
            "--server.enableCORS",
            "false",
            "--server.enableXsrfProtection",
            "false",
        ]
        try:
            rc = stcli.main()
            return rc or 0
        finally:
            sys.argv = sys_argv_backup
    except Exception:
        # Fallback to subprocess if programmatic run fails
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.headless",
            "true",
            "--server.enableCORS",
            "false",
            "--server.enableXsrfProtection",
            "false",
        ]

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        output_buffer: list[str] = []
        if proc.stdout:
            t = threading.Thread(target=stream_reader, args=(proc.stdout, output_buffer), daemon=True)
            t.start()

        # Give Streamlit more time to start (large models or cold-starts can be slow)
        started = wait_for_port(host, port, timeout=120)
        if started:
            url = f"http://{host}:3000"
            try:
                webbrowser.open(url)
            except Exception:
                pass
            proc.wait()
            return proc.returncode or 0

        print("Streamlit did not start within timeout. Recent subprocess output:")
        for line in output_buffer[-200:]:
            print(line, end="")
        proc.wait()
        return proc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
