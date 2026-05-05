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

Если команда `pyinstaller` не находится, это уже учтено: сборка запускается через `python -m PyInstaller`, поэтому отдельная запись в `PATH` не нужна.

Если после сборки нет файла `dist\AudioToText.exe`, значит ошибка произошла до завершения PyInstaller. В этом случае нужен полный текст консоли, особенно строки с ошибкой из этапа `python preload_models.py` или `python -m PyInstaller --clean --noconfirm audio_to_text.spec`.

Скрипт:

- ставит зависимости для сборки;
- заранее скачивает модели `tiny`, `base`, `small`, `medium` в каталог `models`;
- упаковывает приложение в один файл `dist\AudioToText.exe`.

Файл получится большим, потому что модели включаются внутрь сборки.

## GitHub Actions

Если Windows-машины нет, можно собирать `.exe` в GitHub Actions.

Workflow уже добавлен в [build-exe.yml](.github/workflows/build-exe.yml). Он:

- запускается вручную через `Run workflow`;
- может запускаться автоматически при пуше в ветку `main`;
- может запускаться по тегу вида `v1.0.0`;
- может публиковать `.exe` прямо в GitHub Release;
- собирает `AudioToText.exe` на `windows-latest`;
- загружает готовый файл как artifact `AudioToText-windows-exe`.

Чтобы забрать `.exe`:

1. Откройте вкладку Actions в GitHub.
2. Запустите workflow `Build Windows EXE` или дождитесь запуска от push в `main`.
3. Откройте завершённый run и скачайте artifact `AudioToText-windows-exe`.

Чтобы `.exe` попадал сразу в Release:

1. Создайте тег вида `v1.0.0` и отправьте его в GitHub, либо опубликуйте Release в интерфейсе GitHub.
2. Workflow соберёт `AudioToText.exe` на Windows.
3. Готовый файл будет приложен к соответствующему GitHub Release.

## Замечания

- При первом запуске модель будет скачана в локальный кэш.
- `base` запускается быстрее, `small` и `medium` обычно точнее, но работают дольше.
- Если хотите принудительно указать язык, используйте код вроде `ru` или `en`.