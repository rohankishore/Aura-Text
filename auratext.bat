@echo off
setlocal

: Set the script directory to the location of this batch file
set SCRIPT_DIR=%~dp0

: Start Aura Text
echo Starting Aura Text...
python %SCRIPT_DIR%main.py
echo Exiting...

endlocal