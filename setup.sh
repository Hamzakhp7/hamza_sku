#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     🔥 HAMZA SKU - Metasploit C2 Dashboard Setup 🔥      ║"
echo "║   Professional Real Integration - 100% حقيقي              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check Python
echo -e "${YELLOW}[1/5]${NC} Checking Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION found"
else
    echo -e "${RED}✗${NC} Python 3 not found! Please install Python 3.8+"
    exit 1
fi

# Check Metasploit
echo -e "${YELLOW}[2/5]${NC} Checking Metasploit Framework..."
if command -v msfconsole &> /dev/null; then
    echo -e "${GREEN}✓${NC} Metasploit Framework found"
else
    echo -e "${YELLOW}!${NC} Metasploit not found"
    echo -e "${BLUE}[i]${NC} Install it with: sudo apt install metasploit-framework"
fi

# Install Python packages
echo -e "${YELLOW}[3/5]${NC} Installing Python packages..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All packages installed"
else
    echo -e "${RED}✗${NC} Failed to install some packages"
    exit 1
fi

# Create downloads directory
echo -e "${YELLOW}[4/5]${NC} Creating directories..."
mkdir -p downloads
echo -e "${GREEN}✓${NC} Directories created"

# Set permissions
echo -e "${YELLOW}[5/5]${NC} Setting permissions..."
chmod +x c2_server.py
echo -e "${GREEN}✓${NC} Permissions set"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo ""
echo -e "${BLUE}1. Start Metasploit RPC:${NC}"
echo "   msfrpcd -P msf_password -S -a 127.0.0.1"
echo ""
echo -e "${BLUE}2. Start C2 Dashboard:${NC}"
echo "   python3 c2_server.py"
echo ""
echo -e "${BLUE}3. Open your browser:${NC}"
echo "   http://localhost:5000"
echo ""
echo -e "${BLUE}4. Login with password:${NC}"
echo "   hamza_sku_2026"
echo ""
echo -e "${RED}⚠️  IMPORTANT:${NC}"
echo "   • This tool is for AUTHORIZED testing only!"
echo "   • Unauthorized access is ILLEGAL!"
echo "   • Use responsibly and ethically!"
echo ""
