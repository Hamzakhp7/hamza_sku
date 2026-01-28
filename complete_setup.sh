#!/bin/bash

echo "=========================================="
echo "HAMZA SKU C2 Dashboard - Complete Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo -e "${YELLOW}[1/6] Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 not found${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"
echo ""

# Step 2: Check pip
echo -e "${YELLOW}[2/6] Checking pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}ERROR: pip3 not found. Installing...${NC}"
    sudo apt-get update && sudo apt-get install -y python3-pip
fi
echo -e "${GREEN}✓ pip3 is ready${NC}"
echo ""

# Step 3: Install required packages
echo -e "${YELLOW}[3/6] Installing Python packages...${NC}"
echo "This may take a few minutes..."

pip3 install --user Flask==3.0.0 2>&1 | grep -E "(Successfully|Requirement)" || true
pip3 install --user flask-socketio==5.3.5 2>&1 | grep -E "(Successfully|Requirement)" || true
pip3 install --user python-socketio==5.10.0 2>&1 | grep -E "(Successfully|Requirement)" || true
pip3 install --user pymetasploit3==1.0.3 2>&1 | grep -E "(Successfully|Requirement)" || true
pip3 install --user requests==2.31.0 2>&1 | grep -E "(Successfully|Requirement)" || true
pip3 install --user werkzeug==3.0.1 2>&1 | grep -E "(Successfully|Requirement)" || true

echo -e "${GREEN}✓ All packages installed${NC}"
echo ""

# Step 4: Verify installation
echo -e "${YELLOW}[4/6] Verifying installation...${NC}"
python3 << 'PYEOF'
import sys
try:
    import flask
    print(f"✓ Flask {flask.__version__}")
except:
    print("✗ Flask not found")
    sys.exit(1)

try:
    import flask_socketio
    print(f"✓ flask_socketio installed")
except:
    print("✗ flask_socketio not found")
    sys.exit(1)

try:
    import pymetasploit3
    print(f"✓ pymetasploit3 installed")
except:
    print("✗ pymetasploit3 not found")
    sys.exit(1)

try:
    import requests
    print(f"✓ requests {requests.__version__}")
except:
    print("✗ requests not found")
    sys.exit(1)

print("\n✓ All dependencies verified!")
PYEOF

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Dependency check failed${NC}"
    exit 1
fi
echo ""

# Step 5: Create directories
echo -e "${YELLOW}[5/6] Creating directories...${NC}"
mkdir -p downloads templates static
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Step 6: Test server startup
echo -e "${YELLOW}[6/6] Testing server startup...${NC}"
timeout 3 python3 c2_server.py > /tmp/c2_test.log 2>&1 &
SERVER_PID=$!
sleep 2

if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server started successfully!${NC}"
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
else
    echo -e "${RED}✗ Server failed to start${NC}"
    echo "Error log:"
    cat /tmp/c2_test.log
    exit 1
fi
echo ""

# Final instructions
echo "=========================================="
echo -e "${GREEN}✓ SETUP COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "HOW TO START:"
echo ""
echo "1. Start Metasploit RPC (in terminal 1):"
echo "   msfrpcd -P msf_password -S -a 127.0.0.1"
echo ""
echo "2. Start Dashboard (in terminal 2):"
echo "   python3 c2_server.py"
echo ""
echo "3. Open browser:"
echo "   http://localhost:5000"
echo ""
echo "4. Login with:"
echo "   Password: hamza_sku_2026"
echo ""
echo "=========================================="
