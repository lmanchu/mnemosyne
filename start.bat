@echo off
REM Mnemosyne — Start daemon + API server
REM Place shortcut in shell:startup for auto-start on login

set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
set PROJECT=%~dp0
REM Set your Gemini API key as a system environment variable, or uncomment below:
REM set GEMINI_API_KEY=your-key-here
if "%GEMINI_API_KEY%"=="" (
    echo WARNING: GEMINI_API_KEY not set. Daemon will capture only, no analysis.
)
set PYTHONUNBUFFERED=1

REM Activate venv
call "%PROJECT%.venv\Scripts\activate.bat"

REM Start unified daemon + API (single process)
start "Mnemosyne" /min %PYTHON% -u "%PROJECT%app.py"

echo Mnemosyne started.
echo   Daemon: capturing every 10s, analyzing every 15min
echo   API: http://localhost:5700
echo   Console: http://localhost:5700
echo   Onboarding: http://localhost:5700/onboarding
