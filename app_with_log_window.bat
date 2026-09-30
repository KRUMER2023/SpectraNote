@echo off
mode con: cols=85 lines=20
call setup.bat
if %errorlevel% neq 0 exit /b %errorlevel%
python runner.py
