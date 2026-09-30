@echo off
call setup.bat
if %errorlevel% neq 0 exit /b %errorlevel%
start "" pythonw runner.py
