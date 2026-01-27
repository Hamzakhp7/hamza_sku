#!/bin/bash

# HAMZA SKU - Connection Diagnostic Tool - REAL VERSION
# أداة تشخيص الاتصالات - النسخة الحقيقية

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🔍 HAMZA SKU - Connection Diagnostic (REAL)            ║"
echo "║   أداة تشخيص مشاكل الاتصال - حقيقية 100%               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get port from user
read -p "Enter listener port [4444]: " PORT
PORT=${PORT:-4444}

echo ""
echo -e "${BLUE}[*]${NC} Diagnostic started for port ${PORT}..."
echo ""

# Check 1: Dashboard process
echo -e "${YELLOW}[1/8]${NC} Checking Dashboard process..."
if pgrep -f "pentest_dashboard.py" > /dev/null; then
    echo -e "${GREEN}[✓]${NC} Dashboard is running"
    PID=$(pgrep -f "pentest_dashboard.py")
    echo -e "    ${BLUE}→${NC} PID: ${PID}"
else
    echo -e "${RED}[✗]${NC} Dashboard is NOT running!"
    echo -e "${YELLOW}[!]${NC} Start it with: python3 pentest_dashboard.py"
fi
echo ""

# Check 2: Port listening
echo -e "${YELLOW}[2/8]${NC} Checking if port ${PORT} is listening..."
if netstat -tln 2>/dev/null | grep ":${PORT}" > /dev/null || ss -tln 2>/dev/null | grep ":${PORT}" > /dev/null; then
    echo -e "${GREEN}[✓]${NC} Port ${PORT} is listening"
    LISTENING_PID=$(lsof -ti:${PORT} 2>/dev/null)
    if [ ! -z "$LISTENING_PID" ]; then
        LISTENING_PROC=$(ps -p $LISTENING_PID -o comm= 2>/dev/null)
        echo -e "    ${BLUE}→${NC} Process: ${LISTENING_PROC} (PID: ${LISTENING_PID})"
    fi
else
    echo -e "${RED}[✗]${NC} Port ${PORT} is NOT listening!"
    echo -e "${YELLOW}[!]${NC} Make sure you clicked 'START SERVER' in Dashboard"
fi
echo ""

# Check 3: Active connections
echo -e "${YELLOW}[3/8]${NC} Checking for active connections on port ${PORT}..."
CONNECTIONS=$(netstat -tn 2>/dev/null | grep ":${PORT}" | grep ESTABLISHED | wc -l)
if [ "$CONNECTIONS" -gt 0 ]; then
    echo -e "${GREEN}[✓]${NC} Found ${CONNECTIONS} active connection(s):"
    netstat -tn 2>/dev/null | grep ":${PORT}" | grep ESTABLISHED | while read line; do
        REMOTE_IP=$(echo $line | awk '{print $5}' | cut -d: -f1)
        REMOTE_PORT=$(echo $line | awk '{print $5}' | cut -d: -f2)
        echo -e "    ${GREEN}→${NC} ${REMOTE_IP}:${REMOTE_PORT}"
    done
else
    echo -e "${YELLOW}[!]${NC} No active connections found"
    echo -e "${YELLOW}[!]${NC} Possible reasons:"
    echo "        • Payload not running on target"
    echo "        • Firewall blocking connection"
    echo "        • Wrong IP or Port configured"
fi
echo ""

# Check 4: Firewall
echo -e "${YELLOW}[4/8]${NC} Checking firewall status..."
if command -v ufw &> /dev/null; then
    if sudo ufw status 2>/dev/null | grep -q "Status: active"; then
        echo -e "${YELLOW}[!]${NC} UFW firewall is active"
        if sudo ufw status 2>/dev/null | grep -q "${PORT}"; then
            echo -e "${GREEN}[✓]${NC} Port ${PORT} is allowed in firewall"
        else
            echo -e "${RED}[✗]${NC} Port ${PORT} is NOT allowed in firewall!"
            echo -e "${YELLOW}[!]${NC} Allow it with: sudo ufw allow ${PORT}"
        fi
    else
        echo -e "${GREEN}[✓]${NC} UFW firewall is inactive"
    fi
else
    echo -e "${BLUE}[i]${NC} UFW not found, checking iptables..."
    if sudo iptables -L INPUT -n 2>/dev/null | grep -q "${PORT}"; then
        echo -e "${GREEN}[✓]${NC} Port ${PORT} found in iptables"
    else
        echo -e "${YELLOW}[!]${NC} Could not verify iptables rules (might be OK)"
    fi
fi
echo ""

# Check 5: Network interfaces
echo -e "${YELLOW}[5/8]${NC} Listing network interfaces and IPs..."
echo -e "${BLUE}[i]${NC} Your IP addresses:"
ip addr show 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print "    " $2}' | cut -d/ -f1 || \
ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print "    " $2}'
echo ""

# Check 6: Test local connection
echo -e "${YELLOW}[6/8]${NC} Testing local connection to port ${PORT}..."
if timeout 2 nc -zv localhost ${PORT} 2>&1 | grep -q "succeeded\|open"; then
    echo -e "${GREEN}[✓]${NC} Local connection successful"
else
    echo -e "${RED}[✗]${NC} Local connection failed!"
    echo -e "${YELLOW}[!]${NC} The listener might not be properly started"
fi
echo ""

# Check 7: Python packages
echo -e "${YELLOW}[7/8]${NC} Checking Python packages..."
PACKAGES=("Flask" "Flask-SocketIO" "psutil" "eventlet")
MISSING=0
for pkg in "${PACKAGES[@]}"; do
    if python3 -c "import ${pkg,,}" 2>/dev/null; then
        echo -e "${GREEN}[✓]${NC} ${pkg} installed"
    else
        echo -e "${RED}[✗]${NC} ${pkg} NOT installed"
        MISSING=1
    fi
done
if [ $MISSING -eq 1 ]; then
    echo -e "${YELLOW}[!]${NC} Install missing packages with: pip3 install -r requirements.txt"
fi
echo ""

# Check 8: Dashboard accessibility
echo -e "${YELLOW}[8/8]${NC} Testing Dashboard web interface..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200\|302"; then
    echo -e "${GREEN}[✓]${NC} Dashboard web interface is accessible"
else
    echo -e "${RED}[✗]${NC} Dashboard web interface is NOT accessible"
    echo -e "${YELLOW}[!]${NC} Make sure Dashboard is running on port 5000"
fi
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   📊 Diagnostic Summary                                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Status badges
DASHBOARD_OK=0
LISTENER_OK=0
CONNECTIONS_OK=0

if pgrep -f "pentest_dashboard.py" > /dev/null; then DASHBOARD_OK=1; fi
if netstat -tln 2>/dev/null | grep ":${PORT}" > /dev/null || ss -tln 2>/dev/null | grep ":${PORT}" > /dev/null; then LISTENER_OK=1; fi
if [ "$CONNECTIONS" -gt 0 ]; then CONNECTIONS_OK=1; fi

echo -e "Dashboard Status: $([ $DASHBOARD_OK -eq 1 ] && echo -e "${GREEN}✓ Running${NC}" || echo -e "${RED}✗ Not Running${NC}")"
echo -e "Listener Status:  $([ $LISTENER_OK -eq 1 ] && echo -e "${GREEN}✓ Active${NC}" || echo -e "${RED}✗ Inactive${NC}")"
echo -e "Connections:      $([ $CONNECTIONS_OK -eq 1 ] && echo -e "${GREEN}✓ ${CONNECTIONS} Active${NC}" || echo -e "${YELLOW}! None${NC}")"
echo ""

# Recommendations
echo -e "${BLUE}[*]${NC} Recommendations:"
echo ""

if [ $DASHBOARD_OK -eq 0 ]; then
    echo -e "${RED}1. Start Dashboard:${NC}"
    echo "   python3 pentest_dashboard.py"
    echo ""
fi

if [ $LISTENER_OK -eq 0 ] && [ $DASHBOARD_OK -eq 1 ]; then
    echo -e "${YELLOW}2. Start Listener in Dashboard:${NC}"
    echo "   • Open: http://localhost:5000"
    echo "   • Login with: hamza_sku_2026"
    echo "   • Click 'START SERVER' button"
    echo ""
fi

if [ $CONNECTIONS_OK -eq 0 ] && [ $LISTENER_OK -eq 1 ]; then
    echo -e "${YELLOW}3. Connect from target device:${NC}"
    YOUR_IP=$(ip addr show 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | head -1 | awk '{print $2}' | cut -d/ -f1 || \
              ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | head -1 | awk '{print $2}')
    echo "   From your target device, run:"
    echo "   nc ${YOUR_IP} ${PORT}"
    echo ""
    echo "   Then in Dashboard:"
    echo "   • Click '🔍 SCAN' button"
    echo "   • Target should appear in table"
    echo ""
fi

echo -e "${BLUE}[*]${NC} Quick commands:"
echo ""
echo "View real-time connections:"
echo "  ${GREEN}watch -n 1 'netstat -tn | grep :${PORT}'${NC}"
echo ""
echo "Check Dashboard logs:"
echo "  ${GREEN}tail -f /tmp/dashboard.log${NC}"
echo ""
echo "Kill all on port ${PORT}:"
echo "  ${GREEN}sudo lsof -ti:${PORT} | xargs kill -9${NC}"
echo ""
echo "Test connection from another device:"
echo "  ${GREEN}nc -zv YOUR_IP ${PORT}${NC}"
echo ""

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Diagnostic Complete                                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}[*]${NC} For more help, check README.md or TROUBLESHOOTING.md"
