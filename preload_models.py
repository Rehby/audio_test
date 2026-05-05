from __future__ import annotations

from pathlib import Path

from huggingface_hub import snapshot_download


MODELS_DIR = Path(__file__).resolve().parent / "models"
MODEL_OPTIONS = ("tiny", "base", "small", "medium")


def main() -> None:
    MODELS_DIR.mkdir(exist_ok=True)
    for model_name in MODEL_OPTIONS:
        snapshot_download(
            repo_id=f"Systran/faster-whisper-{model_name}",
            local_dir=MODELS_DIR / model_name,
            local_dir_use_symlinks=False,
        )


if __name__ == "__main__":
    main()