@echo off
setlocal

python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

python -m pip install -r requirements.txt -r requirements-build.txt
if errorlevel 1 exit /b 1

python preload_models.py
if errorlevel 1 exit /b 1

python -m PyInstaller --clean --noconfirm audio_to_text.spec
if errorlevel 1 exit /b 1

if not exist dist\AudioToText.exe (
	echo Build finished but dist\AudioToText.exe was not created.
	exit /b 1
)

echo.
echo Ready: dist\AudioToText.exe