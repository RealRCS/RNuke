@echo off
title RNuke
setlocal

:: Check if Python executable exists
python --version 2>&1 | findstr " 3.12" >nul
if %errorlevel% == 0 (
    echo python 3.12.x and up are not supported by RNuke. Please downgrade to python 3.10.x.
    pause
    exit
)

:: Install libraries
echo Installing libraries...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

:: Clear console screen
cls

:: Run the app
echo Running the app...
python app.py

pause
endlocal
