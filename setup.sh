#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   PenTest C2 Dashboard - Setup Script                    ║"
echo "║   تثبيت وإعداد لوحة التحكم                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[+] Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "[!] Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Install requirements
echo ""
echo "[+] Installing required packages..."
pip3 install -r requirements.txt --break-system-packages

if [ $? -ne 0 ]; then
    echo "[!] Failed to install packages. Trying with pip instead of pip3..."
    pip install -r requirements.txt --break-system-packages
fi

# Create necessary directories
echo ""
echo "[+] Creating directories..."
mkdir -p templates
mkdir -p logs

# Set permissions
echo ""
echo "[+] Setting permissions..."
chmod +x pentest_dashboard.py
chmod +x setup.sh

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Setup completed successfully!                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "To run the dashboard:"
echo "  python3 pentest_dashboard.py"
echo ""
echo "Then open your browser at:"
echo "  http://localhost:5000"
echo ""
echo "⚠️  SECURITY WARNING:"
echo "This tool is for authorized penetration testing only!"
echo "Unauthorized access to computer systems is illegal."
echo ""
