@echo off
setlocal
cd /d "%~dp0"
echo Building website...
python build.py
if errorlevel 1 goto failed
git add -- build.py site-data.json dist README.md .gitignore .github "Open Website.cmd" "Upload Website.cmd"
if errorlevel 1 goto failed
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Update academic website"
    if errorlevel 1 goto failed
)
git push origin main
if errorlevel 1 goto failed
echo.
echo Upload complete. GitHub Actions will publish the website.
echo Check: https://github.com/wuyuecon/wuyuecon.github.io/actions
pause
exit /b 0
:failed
echo.
echo Upload stopped. Read the error above. No force push or automatic merge was attempted.
pause
exit /b 1
