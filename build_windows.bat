@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

cd /d "%SCRIPT_DIR%"
if errorlevel 1 exit /b 1

if not exist "%PYTHON_EXE%" (
	echo Creating virtual environment in %VENV_DIR%
	python -m venv "%VENV_DIR%"
	if errorlevel 1 exit /b 1
)

"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

"%PYTHON_EXE%" -m pip install -r "%SCRIPT_DIR%requirements.txt" -r "%SCRIPT_DIR%requirements-build.txt"
if errorlevel 1 exit /b 1

"%PYTHON_EXE%" "%SCRIPT_DIR%preload_models.py"
if errorlevel 1 exit /b 1

"%PYTHON_EXE%" -m PyInstaller --clean --noconfirm "%SCRIPT_DIR%audio_to_text.spec"
if errorlevel 1 exit /b 1

if not exist "%SCRIPT_DIR%dist\AudioToText.exe" (
	echo Build finished but %SCRIPT_DIR%dist\AudioToText.exe was not created.
	exit /b 1
)

echo.
echo Ready: %SCRIPT_DIR%dist\AudioToText.exe