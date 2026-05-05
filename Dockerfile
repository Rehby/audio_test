FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    WHISPER_MODELS=tiny,base,small \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN python -c "import os; from faster_whisper import WhisperModel; [WhisperModel(name.strip(), device='cpu', compute_type='int8') for name in os.environ['WHISPER_MODELS'].split(',') if name.strip()]"

COPY app.py transcriber.py README.md ./

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]