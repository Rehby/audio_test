# Audio to Text

Небольшое локальное приложение для расшифровки аудиофайлов в текст.

## Что умеет

- загрузка аудиофайлов через веб-интерфейс;
- распознавание речи моделью Whisper;
- автоопределение языка или ручной выбор кода языка;
- просмотр сегментов и скачивание результата в `.txt`.

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

После запуска откройте адрес, который покажет Streamlit, обычно `http://localhost:8501`.

## Docker

Сборка образа:

```bash
docker build -t audio-to-text .
```

Запуск контейнера:

```bash
docker run --rm -p 8501:8501 audio-to-text
```

Во время сборки образа контейнер заранее скачивает все модели, доступные в интерфейсе: `tiny`, `base`, `small`, `medium`.

Если хотите сохранить кэш моделей между перезапусками, можно примонтировать каталог:

```bash
docker run --rm -p 8501:8501 \
	-v "$PWD/.cache/huggingface:/root/.cache/huggingface" \
	audio-to-text
```

## Windows EXE

Сборка `AudioToText.exe` делается только на Windows, потому что PyInstaller не собирает Windows `.exe` из macOS.

Шаги:

```bat
python -m venv .venv
.venv\Scripts\activate
build_windows.bat
```

Скрипт:

- ставит зависимости для сборки;
- заранее скачивает модели `tiny`, `base`, `small`, `medium` в каталог `models`;
- упаковывает приложение в один файл `dist\AudioToText.exe`.

Файл получится большим, потому что модели включаются внутрь сборки.

## Замечания

- При первом запуске модель будет скачана в локальный кэш.
- `base` запускается быстрее, `small` и `medium` обычно точнее, но работают дольше.
- Если хотите принудительно указать язык, используйте код вроде `ru` или `en`.