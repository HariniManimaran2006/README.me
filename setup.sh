#!/bin/bash
# Contract Auditor Setup Script for macOS/Linux

echo "========================================"
echo "Contract Auditor - Setup Script"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "Python found. Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the Contract Auditor app:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run app: streamlit run app.py"
echo ""
