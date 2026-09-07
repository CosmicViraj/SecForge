@echo off
title Build CyberLab Suite
echo ======================================
echo        CyberLab Suite Builder
echo ======================================
echo.
python --version
if errorlevel 1 (
    echo Python is not installed or is not on PATH.
    pause
    exit /b 1
)

echo Installing build dependency...
python -m pip install -r requirements.txt

echo.
echo Building Windows EXE...
python -m PyInstaller --onefile --windowed --name "CyberLabSuite" cyberlab_suite.py

echo.
echo Build complete.
echo EXE: dist\CyberLabSuite.exe
pause
