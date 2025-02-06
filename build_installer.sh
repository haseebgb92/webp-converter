#!/bin/bash

echo "Building WebP Converter Installer..."

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Build executable
pyinstaller build_exe.spec

# Create installer
makensis installer.nsi

echo "Build complete! You can find WebPConverter_Setup.exe in the current directory."
