import subprocess
import sys
import time
import webbrowser
import socket
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


def main() -> int:
    project_dir = Path(__file__).parent
    app_path = project_dir / "app.py"
    if not app_path.exists():
        print("Error: app.py not found next to launcher.py")
        return 2

    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.headless", "true"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    host = "127.0.0.1"
    port = 8501

    if wait_for_port(host, port, timeout=60):
        url = f"http://{host}:{port}"
        try:
            webbrowser.open(url)
        except Exception:
            pass
        proc.wait()
        return proc.returncode or 0

    print("Streamlit did not start within timeout. Showing subprocess output:")
    if proc.stdout:
        for line in proc.stdout:
            print(line, end="")
    proc.wait()
    return proc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
