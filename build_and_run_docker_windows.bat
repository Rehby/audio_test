@echo off
REM build_and_run_docker_windows.bat
REM Wrapper to run the PowerShell helper with elevation (UAC prompt).
REM Usage: double-click or run from cmd: build_and_run_docker_windows.bat [--ImageName name] [--Port 8501] [-Build:$true|$false]

setlocal

REM Resolve script path
set "SCRIPT=%~dp0build_and_run_docker_windows.ps1"

if not exist "%SCRIPT%" (
    echo PowerShell helper not found: %SCRIPT%
    pause
    exit /b 1
)

REM Launch elevated PowerShell that runs the script and forwards arguments
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" %*' -Verb RunAs"
