@echo off
:: Ensure the script runs from its own folder
cd /d "%~dp0"

echo 🐉 Launching Project Creator...

:: Run the script directly
python main.py

:: If it crashes or finishes, this stops the window from vanishing
echo.
echo Press any key to exit.
pause >nul