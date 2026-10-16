@echo off
setlocal EnableExtensions
cd /d "%~dp0.."

rem Cach dung: scripts\docker-push.bat ^<repository^> [tag]
rem   Docker Hub:  scripts\docker-push.bat <username>/be-face-v1 1.0.0
rem   GHCR:        scripts\docker-push.bat ghcr.io/<org>/be-face-v1 1.0.0
rem   Registry rieng: scripts\docker-push.bat registry.company.com/<team>/be-face-v1 1.0.0
set "REPO=%~1"
set "TAG=%~2"
if "%REPO%"=="" (
    echo Cach dung: scripts\docker-push.bat ^<repository^> [tag]
    echo   Vi du: scripts\docker-push.bat myuser/be-face-v1 1.0.0
    exit /b 1
)
if "%TAG%"=="" set "TAG=latest"

docker image inspect be-face-v1:%TAG% >nul 2>&1
if errorlevel 1 (
    echo [docker-push] Chua co image be-face-v1:%TAG%. Chay truoc: scripts\docker-build.bat %TAG%
    exit /b 1
)

docker tag be-face-v1:%TAG% %REPO%:%TAG% || exit /b 1
docker push %REPO%:%TAG%
if errorlevel 1 (
    echo [docker-push] Push that bai. Kiem tra da "docker login" vao registry chua.
    exit /b 1
)

if /i not "%TAG%"=="latest" (
    docker tag be-face-v1:%TAG% %REPO%:latest || exit /b 1
    docker push %REPO%:latest || exit /b 1
)

echo [docker-push] Xong: %REPO%:%TAG%
exit /b 0
