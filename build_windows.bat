@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

cd /d "%SCRIPT_DIR%"
if errorlevel 1 exit /b 1

python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

python -m pip install -r "%SCRIPT_DIR%requirements.txt" -r "%SCRIPT_DIR%requirements-build.txt"
if errorlevel 1 exit /b 1

python "%SCRIPT_DIR%preload_models.py"
if errorlevel 1 exit /b 1

python -m PyInstaller --clean --noconfirm "%SCRIPT_DIR%audio_to_text.spec"
if errorlevel 1 exit /b 1

if not exist "%SCRIPT_DIR%dist\AudioToText.exe" (
	echo Build finished but %SCRIPT_DIR%dist\AudioToText.exe was not created.
	exit /b 1
)

echo.
echo Ready: %SCRIPT_DIR%dist\AudioToText.exe