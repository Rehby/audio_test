
import os
import sys


def _bundle_path() -> str:
	# When bundled by PyInstaller, resources are extracted to _MEIPASS
	return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
	try:
		# Streamlit >=1.0
		from streamlit.web import cli as stcli
	except Exception:
		import streamlit.cli as stcli

	base = _bundle_path()
	app_path = os.path.join(base, "app.py")

	# Ensure the script exists (helps when running from source)
	if not os.path.exists(app_path):
		# Try relative path from cwd as a fallback
		app_path = os.path.join(os.getcwd(), "app.py")

	sys.argv = ["streamlit", "run", app_path, "--server.headless", "true"]

	return stcli.main()


if __name__ == "__main__":
	raise SystemExit(main())

