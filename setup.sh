#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🔥 HAMZA SKU C2 Dashboard - Real Version Setup         ║"
echo "║   إعداد لوحة التحكم الحقيقية 100%                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python
echo -e "${YELLOW}[1/4]${NC} Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION found"
else
    echo -e "${RED}✗${NC} Python 3 not found! Please install Python 3.8+"
    exit 1
fi

# Check pip
echo -e "${YELLOW}[2/4]${NC} Checking pip..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip3 found"
else
    echo -e "${RED}✗${NC} pip3 not found! Installing..."
    sudo apt-get install -y python3-pip
fi

# Install requirements
echo -e "${YELLOW}[3/4]${NC} Installing Python packages..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All packages installed successfully"
else
    echo -e "${RED}✗${NC} Failed to install some packages"
    exit 1
fi

# Check netcat
echo -e "${YELLOW}[4/4]${NC} Checking netcat (nc)..."
if command -v nc &> /dev/null; then
    echo -e "${GREEN}✓${NC} netcat found"
else
    echo -e "${YELLOW}!${NC} netcat not found. Installing..."
    sudo apt-get install -y netcat-traditional netcat-openbsd 2>/dev/null
fi

# Set permissions
chmod +x pentest_dashboard.py 2>/dev/null
chmod +x setup.sh 2>/dev/null

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}To start the dashboard:${NC}"
echo "  python3 pentest_dashboard.py"
echo ""
echo -e "${GREEN}Then open your browser:${NC}"
echo "  http://localhost:5000"
echo ""
echo -e "${GREEN}Login with:${NC}"
echo "  Password: hamza_sku_2026"
echo ""
echo -e "${RED}⚠️  IMPORTANT SECURITY WARNING:${NC}"
echo "  • This tool is for AUTHORIZED penetration testing ONLY"
echo "  • Unauthorized access to systems is ILLEGAL"
echo "  • Use only in controlled environments"
echo "  • Always get written permission before testing"
echo ""
