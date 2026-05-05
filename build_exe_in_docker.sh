#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="audio-to-text-exe-builder"
CONTAINER_NAME="audio-to-text-exe-export"
PLATFORM="linux/amd64"
HOST_ARCH="$(uname -m)"

cd "$SCRIPT_DIR"

if [[ "$HOST_ARCH" == "arm64" || "$HOST_ARCH" == "aarch64" ]]; then
  if [[ "${ALLOW_UNSUPPORTED_ARM_WINE:-0}" != "1" ]]; then
    cat <<'EOF'
Detected Apple Silicon / ARM host.

This Docker path uses a Wine-based amd64 image. On Apple Silicon it is not reliable and in practice often aborts inside wineboot before pip or PyInstaller starts.

Use one of these instead:
1. GitHub Actions workflow already configured in this repository.
2. Native Windows build via build_windows.bat.

If you still want to try the unsupported ARM path, rerun with:
ALLOW_UNSUPPORTED_ARM_WINE=1 ./build_exe_in_docker.sh
EOF
    exit 1
  fi
fi

docker build --platform "$PLATFORM" -f Dockerfile.winexe -t "$IMAGE_NAME" .

mkdir -p dist

if docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
  docker rm -f "$CONTAINER_NAME" >/dev/null
fi

docker create --platform "$PLATFORM" --name "$CONTAINER_NAME" "$IMAGE_NAME" >/dev/null
docker cp "$CONTAINER_NAME:/AudioToText.exe" "$SCRIPT_DIR/dist/AudioToText.exe"
docker rm "$CONTAINER_NAME" >/dev/null

echo "Ready: $SCRIPT_DIR/dist/AudioToText.exe"