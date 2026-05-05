@echo off
setlocal

python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-build.txt
python preload_models.py
pyinstaller --clean --noconfirm audio_to_text.spec

echo.
echo Ready: dist\AudioToText.exe