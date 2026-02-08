@echo off
REM Local Docker Test Script for Phase 3 Backend (Windows)

echo.
echo ==========================================
echo Phase 3 Backend - Local Docker Test
echo ==========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env file with your actual values:
    echo   1. DATABASE_URL - Your Neon database URL
    echo   2. BETTER_AUTH_SECRET - Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
    echo   3. OPENROUTER_API_KEY - Get from https://openrouter.ai/keys
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo Loading environment variables from .env...
for /f "tokens=*" %%a in (.env) do (
    set "%%a"
)

REM Verify required variables
if "%DATABASE_URL%"=="" (
    echo ERROR: DATABASE_URL is not set in .env file
    pause
    exit /b 1
)

if "%BETTER_AUTH_SECRET%"=="" (
    echo ERROR: BETTER_AUTH_SECRET is not set in .env file
    pause
    exit /b 1
)

if "%OPENROUTER_API_KEY%"=="" (
    echo ERROR: OPENROUTER_API_KEY is not set in .env file
    pause
    exit /b 1
)

echo ✓ All required environment variables are set
echo.

REM Build Docker image
echo Building Docker image...
docker build -t phase3-backend .

if %errorlevel% neq 0 (
    echo ERROR: Docker build failed
    pause
    exit /b 1
)

echo ✓ Docker image built successfully
echo.

REM Run container
echo Starting container on port 7860...
docker run -p 7860:7860 ^
  -e DATABASE_URL=%DATABASE_URL% ^
  -e BETTER_AUTH_SECRET=%BETTER_AUTH_SECRET% ^
  -e OPENROUTER_API_KEY=%OPENROUTER_API_KEY% ^
  -e OPENROUTER_MODEL=%OPENROUTER_MODEL% ^
  -e FRONTEND_URL=%FRONTEND_URL% ^
  --name phase3-backend ^
  phase3-backend

echo.
echo Container stopped. To remove:
echo   docker rm phase3-backend
echo.
pause
