@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo Chua co venv. Chay: py -3.11 -m venv venv ^&^& venv\Scripts\pip install -r requirements.txt
    exit /b 1
)
set HOST=0.0.0.0
set PORT=8001
venv\Scripts\python.exe run_server.py
