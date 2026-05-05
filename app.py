from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from transcriber import MODEL_OPTIONS, TranscriptionError, transcribe_audio


st.set_page_config(
    page_title="Audio to Text",
    page_icon="🎙️",
    layout="wide",
)


SUPPORTED_TYPES = [
    "mp3",
    "wav",
    "m4a",
    "ogg",
    "flac",
    "aac",
    "mp4",
    "mpeg",
    "webm",
]


def save_uploaded_file(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> Path:
    suffix = Path(uploaded_file.name).suffix or ".tmp"
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return Path(temp_file.name)


st.title("Audio to Text")
st.write(
    "Загрузите аудиофайл, выберите модель и получите расшифровку. "
    "В Docker-образе доступные модели уже предзагружены."
)

with st.sidebar:
    st.header("Настройки")
    model_name = st.selectbox(
        "Модель Whisper",
        options=MODEL_OPTIONS,
        index=1,
        help="`base` быстрее, `small` и `medium` обычно точнее.",
    )
    language = st.text_input(
        "Язык речи",
        value="",
        help="Оставьте пустым для автоопределения. Пример: ru, en, de.",
    ).strip() or None

uploaded_file = st.file_uploader(
    "Аудиофайл",
    type=SUPPORTED_TYPES,
    accept_multiple_files=False,
)

if uploaded_file is not None:
    st.audio(uploaded_file)

    if st.button("Распознать", type="primary"):
        temp_path = save_uploaded_file(uploaded_file)
        try:
            with st.spinner("Распознаю аудио..."):
                result = transcribe_audio(
                    file_path=temp_path,
                    model_name=model_name,
                    language=language,
                )
        except TranscriptionError as error:
            st.error(str(error))
        finally:
            temp_path.unlink(missing_ok=True)

        if "result" in locals():
            st.subheader("Результат")
            st.text_area(
                "Текст",
                value=result.text,
                height=280,
            )
            st.download_button(
                "Скачать TXT",
                data=result.text,
                file_name=f"{Path(uploaded_file.name).stem}.txt",
                mime="text/plain",
            )

            col1, col2, col3 = st.columns(3)
            col1.metric("Язык", result.language.upper())
            col2.metric("Вероятность", f"{result.language_probability:.2f}")
            col3.metric("Сегментов", str(len(result.segments)))

            with st.expander("Сегменты"):
                for index, segment in enumerate(result.segments, start=1):
                    st.write(
                        f"{index}. [{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}"
                    )
else:
    st.info("Поддерживаются MP3, WAV, M4A, OGG, FLAC, AAC, MP4, MPEG и WEBM.")