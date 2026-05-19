@echo off
setlocal

cd /d "%~dp0"

echo Starting backend and frontend with Docker...
docker compose up --build -d
if errorlevel 1 (
    echo.
    echo Failed to start Docker containers.
    echo Make sure Docker Desktop is running, then try again.
    pause
    exit /b 1
)

echo.
echo Waiting for the web app to become available...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$deadline = (Get-Date).AddSeconds(60); " ^
  "$ready = $false; " ^
  "while ((Get-Date) -lt $deadline) { " ^
  "  try { " ^
  "    $backend = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' -TimeoutSec 3; " ^
  "    $frontend = Invoke-WebRequest -Uri 'http://127.0.0.1:8080' -UseBasicParsing -TimeoutSec 3; " ^
  "    if ($backend.status -eq 'ok' -and $frontend.StatusCode -eq 200) { $ready = $true; break } " ^
  "  } catch { Start-Sleep -Seconds 2 } " ^
  "} " ^
  "if (-not $ready) { exit 1 }"

if errorlevel 1 (
    echo.
    echo Containers started, but the site did not respond in time.
    echo Try opening http://127.0.0.1:8080 manually in a minute.
    docker compose ps
    pause
    exit /b 1
)

echo.
echo Opening frontend: http://127.0.0.1:8080/?v=latest
start "" "http://127.0.0.1:8080/?v=latest"

echo.
echo Project is running.
echo Frontend: http://127.0.0.1:8080/?v=latest
echo Backend docs: http://127.0.0.1:8000/docs
echo.
echo To stop the project, run:
echo docker compose down
echo.
pause
