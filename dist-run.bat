@echo off
cd /d "%~dp0"
if not exist "dist\be-face.exe" (
    echo Chua build. Chay build.bat truoc.
    exit /b 1
)
set HOST=0.0.0.0
set PORT=8000
dist\be-face.exe
