@echo off
echo Running Photobooth Layout Tool (GUI)...
python photobooth_layout_tool.py
if errorlevel 1 (
    echo Error occurred. Make sure Python is installed and required packages are available.
    echo You can install requirements by running: install.bat
    pause
)