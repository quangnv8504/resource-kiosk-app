@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY=%~dp0venv\Scripts\python.exe"

echo === BE Face - Build ONEFILE EXE (InsightFace + ONNX) ===
echo Can Python 3.11
echo.

if not exist "%PY%" (
    echo Tao venv Python 3.11...
    py -3.11 -m venv venv
    if errorlevel 1 (
        echo Loi: Khong tao duoc venv. Cai Python 3.11 tu python.org
        exit /b 1
    )
)

if not exist "%PY%" (
    echo Loi: Khong tim thay %PY%
    exit /b 1
)

echo Python:
"%PY%" --version
echo.

echo Cai dependencies...
"%PY%" -m pip install --upgrade pip
if errorlevel 1 goto :fail

"%PY%" -m pip install -r requirements.txt
if errorlevel 1 goto :fail

"%PY%" -m pip install pyinstaller
if errorlevel 1 goto :fail

call scripts\prepare_models.bat
if errorlevel 1 goto :fail

echo.
echo Build PyInstaller ONEFILE (dist\be-face.exe, co the mat 5-15 phut)...

REM Dung be-face.exe neu dang chay — neu khong, PyInstaller khong ghi de duoc file exe
tasklist /FI "IMAGENAME eq be-face.exe" 2>nul | find /I "be-face.exe" >nul
if not errorlevel 1 (
    echo Dang dung be-face.exe cu...
    taskkill /F /IM be-face.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
)

if exist "dist\be-face" rmdir /s /q "dist\be-face"
if exist "dist\be-face.exe" (
    del /f /q "dist\be-face.exe" 2>nul
    if exist "dist\be-face.exe" (
        echo.
        echo LOI: Khong xoa duoc dist\be-face.exe ^(file dang bi khoa^).
        echo - Dong cua so dist-run.bat / be-face.exe
        echo - Hoac mo Task Manager, ket thuc tien trinh be-face.exe
        echo - Chay lai build.bat
        goto :fail
    )
)

"%PY%" -m PyInstaller --noconfirm --clean be-face.spec
if errorlevel 1 goto :fail

echo.
echo === Build thanh cong ===
echo Output: dist\be-face.exe
echo Chay: .\dist-run.bat
echo API: http://127.0.0.1:8001/api/v1/compare
echo.
pause
exit /b 0

:fail
echo.
echo Build THAT BAI.
pause
exit /b 1
