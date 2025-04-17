#!/bin/bash
echo "Running Photobooth PSD Layer Extractor..."
python3 photobooth_psd_extractor.py "$@"
if [ $? -ne 0 ]; then
    echo "Error occurred. Make sure Python is installed and psd-tools package is available."
    echo "You can install requirements by running: ./install.sh"
    read -p "Press Enter to continue..."
fi