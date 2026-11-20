@echo off
title Legacy Android & XDA Hardware Bench
if not exist ".venv" (
    echo [*] Setting up Python virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)
python android_bench.py
pause
