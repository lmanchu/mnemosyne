@echo off
REM Mnemosyne — Start daemon + API server
REM Place shortcut in shell:startup for auto-start on login

set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
set PROJECT=%~dp0
set GEMINI_API_KEY=AIzaSyCmNaW3sEVT8cCEjy3GijQjqRxyWIoJTdM
set PYTHONUNBUFFERED=1

REM Activate venv
call "%PROJECT%.venv\Scripts\activate.bat"

REM Start daemon (background)
start "Mnemosyne Daemon" /min %PYTHON% -u "%PROJECT%daemon.py"

REM Start API server (background)
start "Mnemosyne API" /min %PYTHON% -u "%PROJECT%api.py"

echo Mnemosyne started.
echo   Daemon: capturing every 10s, analyzing every 15min
echo   API: http://localhost:5700
echo   Console: http://localhost:5700
echo   Onboarding: http://localhost:5700/onboarding
