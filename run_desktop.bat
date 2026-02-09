@echo off
echo Starting Desktop Application...
cd desktop
call ..\backend\venv\Scripts\activate
python main.py
pause
