from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from faster_whisper import WhisperModel


MODEL_OPTIONS = ("tiny", "base", "small", "medium")


class TranscriptionError(Exception):
    pass


@dataclass(frozen=True)
class SegmentResult:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class TranscriptionResult:
    text: str
    language: str
    language_probability: float
    segments: list[SegmentResult]


@lru_cache(maxsize=4)
def load_model(model_name: str) -> WhisperModel:
    return WhisperModel(resolve_model_source(model_name), device="cpu", compute_type="int8")


def resolve_model_source(model_name: str) -> str:
    bundled_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    bundled_model = bundled_root / "models" / model_name
    if bundled_model.exists():
        return str(bundled_model)

    local_model = Path(__file__).resolve().parent / "models" / model_name
    if local_model.exists():
        return str(local_model)

    return model_name


def transcribe_audio(file_path: Path, model_name: str, language: str | None) -> TranscriptionResult:
    if not file_path.exists():
        raise TranscriptionError("Загруженный файл не найден.")

    try:
        model = load_model(model_name)
        segments, info = model.transcribe(
            str(file_path),
            language=language,
            vad_filter=True,
            beam_size=5,
        )
        segment_list = [
            SegmentResult(start=segment.start, end=segment.end, text=segment.text.strip())
            for segment in segments
            if segment.text.strip()
        ]
    except Exception as error:
        raise TranscriptionError(f"Не удалось распознать аудио: {error}") from error

    if not segment_list:
        raise TranscriptionError("Модель не вернула текст. Проверьте качество аудио.")

    transcript = "\n".join(segment.text for segment in segment_list)
    return TranscriptionResult(
        text=transcript,
        language=info.language,
        language_probability=info.language_probability,
        segments=segment_list,
    )