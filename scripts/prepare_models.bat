@echo off
setlocal EnableExtensions
cd /d "%~dp0.."

set "DEST=models\buffalo_l"
set "SRC=%USERPROFILE%\.insightface\models\buffalo_l"

if not exist "%DEST%" mkdir "%DEST%"

for %%F in (det_10g.onnx w600k_r50.onnx) do (
    if not exist "%DEST%\%%F" (
        if exist "%SRC%\%%F" (
            echo [prepare_models] Copy %%F...
            copy /Y "%SRC%\%%F" "%DEST%\" >nul
        ) else (
            echo [prepare_models] Thieu %%F — chay lan dau trong venv:
            echo   venv\Scripts\python -c "from insightface.app import FaceAnalysis; FaceAnalysis(name='buffalo_l').prepare(ctx_id=-1)"
            exit /b 1
        )
    ) else (
        echo [prepare_models] Da co %%F
    )
)

echo [prepare_models] Xong.
exit /b 0
