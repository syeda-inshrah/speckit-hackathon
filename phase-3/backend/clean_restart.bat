@echo off
echo Killing all Python processes...
taskkill /F /IM python.exe 2>nul

echo Waiting for processes to terminate...
timeout /t 3 /nobreak >nul

echo Starting backend server...
cd /d "%~dp0"
python app.py
