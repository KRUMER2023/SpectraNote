app_with_log_window@echo off
mode con: cols=75 lines=10
call .venv\Scripts\activate.bat
python runner.py
