@echo OFF

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not defined in enviromental variables. Please define it.
    timeout /t 5 /nobreak
    exit
)

python -c "import psutil" 2>nul || python -m pip install psutil
`
python -c "import pystray" 2>nul || python -m pip install pystray

start /min pythonw RAMusage.py
start /min pythonw CPUusage.py
start /min pythonw Cspace.py
@REM start /min pythonw Battery.py

timeout /t 1 /nobreak 

exit
