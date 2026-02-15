@echo off
REM Kill all Python processes on port 7860
echo Stopping all servers on port 7860...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :7860 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo Done!
timeout /t 2 /nobreak >nul

echo Starting fresh server...
cd /d "%~dp0"
python app.py
