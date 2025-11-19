@echo off
setlocal enabledelayedexpansion

title Speech to Text (Thai) - Launcher
cd /d "%~dp0"

:: -----------------------------------------
::  SPLASH SCREEN
:: -----------------------------------------
cls
echo ====================================================
echo               Speech to Text (Thai)
echo ====================================================
echo                   by Supawat Arrakrattakun
echo ----------------------------------------------------
echo                Checking system components...
echo ====================================================
echo.

timeout /t 1 >nul

:: -----------------------------------------
::  CHECK PYTHON PORTABLE
:: -----------------------------------------
if not exist "python\pythonw.exe" (
    echo [ERROR] Python portable not found!
    echo Please make sure: python\pythonw.exe exists.
    pause
    exit /b
) else (
    echo [OK] Python portable found.
)

timeout /t 1 >nul

:: -----------------------------------------
::  CHECK DEPENDENCIES INSTALLED
:: -----------------------------------------
echo Checking Python dependencies...
python\python.exe -c "import pyaudio, pydub, speech_recognition" 2>nul

if %errorlevel% neq 0 (
    echo [ERROR] Dependencies are not installed.
    echo Installing dependencies from requirements.txt ...
    python\python.exe -m pip install -r requirements.txt --prefix python
    echo Dependencies installed.
) else (
    echo [OK] Dependencies are ready.
)

timeout /t 1 >nul

:: -----------------------------------------
::  CHECK FFMPEG
:: -----------------------------------------
set FF=ffmpeg\bin\ffmpeg.exe

if not exist "%FF%" (
    echo [ERROR] FFmpeg not found!
    echo Please put FFmpeg in: ffmpeg\bin\ffmpeg.exe
    pause
    exit /b
) else (
    echo [OK] FFmpeg is ready.
)

timeout /t 1 >nul

:: -----------------------------------------
::  FINISH SPLASH
:: -----------------------------------------
cls
echo ====================================================
echo               Speech to Text (Thai)
echo ----------------------------------------------------
echo                All checks passed.
echo                Starting application...
echo ====================================================
timeout /t 1 >nul

:: -----------------------------------------
::  RUN PROGRAM (GUI ONLY - NO CONSOLE)
:: -----------------------------------------
start "" python\pythonw.exe main.py

exit /b
