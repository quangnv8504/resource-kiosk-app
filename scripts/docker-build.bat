@echo off
setlocal EnableExtensions
cd /d "%~dp0.."

rem Cach dung: scripts\docker-build.bat [tag]   (mac dinh: latest)
set "TAG=%~1"
if "%TAG%"=="" set "TAG=latest"

call scripts\prepare_models.bat || exit /b 1

echo [docker-build] Build be-face-v1:%TAG% ...
docker build --platform linux/amd64 -t be-face-v1:%TAG% . || exit /b 1

if /i not "%TAG%"=="latest" (
    docker tag be-face-v1:%TAG% be-face-v1:latest || exit /b 1
)

echo [docker-build] Xong: be-face-v1:%TAG%
exit /b 0
