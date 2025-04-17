#!/bin/bash
echo "Installing required packages for Photobooth Layout Tool..."
python3 -m pip install --upgrade pip
python3 -m pip install psd-tools

if [ $? -ne 0 ]; then
    echo "Error occurred during installation."
    echo "Please make sure Python is installed correctly."
    echo "If you don't have Python installed, use your package manager or visit https://www.python.org/downloads/"
    read -p "Press Enter to continue..."
else
    echo "Installation complete!"
    echo ""
    echo "You can now run the tool using:"
    echo " - Command-line version: ./start.sh"
    echo " - Graphical interface: ./start_ui.sh"

    # Make the script files executable
    chmod +x start.sh
    chmod +x start_ui.sh
    chmod +x photobooth_psd_extractor.py
    chmod +x photobooth_layout_tool.py

    read -p "Press Enter to continue..."
fi