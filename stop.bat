@echo off
REM Mnemosyne — Stop daemon + API server
taskkill /FI "WINDOWTITLE eq Mnemosyne Daemon" /F 2>nul
taskkill /FI "WINDOWTITLE eq Mnemosyne API" /F 2>nul
echo Mnemosyne stopped.
