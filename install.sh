#!/bin/bash

echo "Installing C2 Dashboard..."

# Install packages
pip3 install --user Flask pymetasploit3 --quiet

echo "✓ Installation complete"
echo ""
echo "To start:"
echo "1. Terminal 1: msfrpcd -P msf_password -a 127.0.0.1"
echo "2. Terminal 2: python3 server.py"
echo "3. Browser: http://localhost:5000"
echo "4. Password: admin"
