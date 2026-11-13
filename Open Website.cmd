@echo off
cd /d "%~dp0"
python build.py
if errorlevel 1 goto failed
start "" "%~dp0docs\index.html"
exit /b 0
:failed
echo Preview stopped. Check site-data.json and the error above.
pause
exit /b 1
