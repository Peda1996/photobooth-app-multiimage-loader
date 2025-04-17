@echo off
echo Running Photobooth PSD Layer Extractor...
python photobooth_psd_extractor.py %*
if errorlevel 1 (
    echo Error occurred. Make sure Python is installed and psd-tools package is available.
    echo You can install requirements by running: install.bat
    pause
)