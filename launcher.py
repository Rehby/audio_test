
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

	# Build Streamlit CLI args. Allow configuration via environment variables
	# or by passing extra args to the exe (they will be forwarded).
	user_args = sys.argv[1:]

	args = ["streamlit", "run", app_path, "--server.headless", "true"]

	addr = os.environ.get("STREAMLIT_ADDRESS") or os.environ.get("STREAMLIT_HOST")
	port = os.environ.get("STREAMLIT_PORT")

	if addr:
		args += ["--server.address", addr]
	if port:
		args += ["--server.port", port]

	# Allow toggling CORS / XSRF protection via env vars. Accepted names:
	# STREAMLIT_ENABLECORS, STREAMLIT_SERVER_ENABLECORS
	# STREAMLIT_ENABLEXSRFPROTECTION, STREAMLIT_SERVER_ENABLEXSRFPROTECTION
	def _env_bool(*names):
		for n in names:
			v = os.environ.get(n)
			if v is not None:
				return v
		return None

	cors = _env_bool("STREAMLIT_ENABLECORS", "STREAMLIT_SERVER_ENABLECORS")
	xsrf = _env_bool(
		"STREAMLIT_ENABLEXSRFPROTECTION", "STREAMLIT_SERVER_ENABLEXSRFPROTECTION"
	)

	if cors is not None:
		args += ["--server.enableCORS", cors]
	if xsrf is not None:
		args += ["--server.enableXsrfProtection", xsrf]

	# Forward any additional user-provided args (e.g. -- --server.enableCORS false)
	if user_args:
		args += user_args

	sys.argv = args

	return stcli.main()


if __name__ == "__main__":
	raise SystemExit(main())

