@echo off
REM Quick Vercel Deployment Script for Phase 3 Frontend (Windows)

echo 🚀 Deploying Phase 3 Frontend to Vercel...
echo.

REM Navigate to frontend directory
cd /d "%~dp0frontend"

REM Check if vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Installing Vercel CLI...
    npm install -g vercel
)

REM Login to Vercel
echo 🔐 Logging in to Vercel...
call vercel login

REM Deploy to production
echo 🌐 Deploying to production...
call vercel --prod

echo.
echo ✅ Deployment complete!
echo.
echo 📝 Don't forget to set environment variable:
echo    vercel env add NEXT_PUBLIC_API_URL production
echo    Value: https://syeda-inshrah-speckit.hf.space
echo.
echo Then redeploy:
echo    vercel --prod
echo.
pause
