@echo off
echo Installing required packages for Photobooth Layout Tool...
python -m pip install --upgrade pip
python -m pip install psd-tools tkinter
if errorlevel 1 (
    echo Error occurred during installation.
    echo Please make sure Python is installed correctly.
    echo If you don't have Python installed, download it from https://www.python.org/downloads/
    pause
) else (
    echo Installation complete!
    echo.
    echo You can now run the tool using:
    echo  - Command-line version: start.bat
    echo  - Graphical interface: start_ui.bat
    pause
)