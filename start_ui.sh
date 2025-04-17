#!/bin/bash
echo "Running Photobooth Layout Tool (GUI)..."
python3 photobooth_layout_tool.py
if [ $? -ne 0 ]; then
    echo "Error occurred. Make sure Python is installed and required packages are available."
    echo "You can install requirements by running: ./install.sh"
    read -p "Press Enter to continue..."
fi