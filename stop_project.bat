@echo off
setlocal

cd /d "%~dp0"

echo Stopping Docker containers...
docker compose down

echo.
echo Project stopped.
pause
