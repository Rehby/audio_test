@echo off
REM build_windows.bat — собирает dist\AudioToText.exe на Windows
setlocal enabledelayedexpansion

REM 1) Создаём виртуальное окружение (.venv) если нужно и активируем
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM 2) (Опционально) предзагрузить модели в каталог models
if exist preload_models.py (
    python preload_models.py
) else (
    echo preload_models.py не найден — пропускаю предзагрузку моделей
)

REM 3) Собираем exe через PyInstaller, используя готовый spec-файл
python -m PyInstaller --clean --noconfirm audio_to_text.spec

REM 4) Переносим итоговый exe в release\
if not exist release (
    mkdir release
)
if exist dist\AudioToText.exe (
    move /Y dist\AudioToText.exe release\AudioToText.exe
    echo Готово: release\AudioToText.exe
) else (
    echo Ошибка: dist\AudioToText.exe не найден. Проверьте вывод PyInstaller.
)

pause
