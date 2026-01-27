#!/bin/bash

# HAMZA SKU - Connection Diagnostic Tool
# أداة تشخيص الاتصالات

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🔍 HAMZA SKU - Connection Diagnostic                   ║"
echo "║   أداة تشخيص مشاكل الاتصال                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get port from user
read -p "Enter listener port [443]: " PORT
PORT=${PORT:-443}

echo ""
echo -e "${BLUE}[*]${NC} Diagnostic started for port ${PORT}..."
echo ""

# Check 1: Dashboard process
echo -e "${YELLOW}[1/6]${NC} Checking Dashboard process..."
if pgrep -f "pentest_dashboard.py" > /dev/null; then
    echo -e "${GREEN}[✓]${NC} Dashboard is running"
else
    echo -e "${RED}[✗]${NC} Dashboard is NOT running!"
    echo -e "${YELLOW}[!]${NC} Start it with: python3 pentest_dashboard.py"
fi
echo ""

# Check 2: Port listening
echo -e "${YELLOW}[2/6]${NC} Checking if port ${PORT} is listening..."
if netstat -tln | grep ":${PORT}" > /dev/null 2>&1 || ss -tln | grep ":${PORT}" > /dev/null 2>&1; then
    echo -e "${GREEN}[✓]${NC} Port ${PORT} is listening"
else
    echo -e "${RED}[✗]${NC} Port ${PORT} is NOT listening!"
    echo -e "${YELLOW}[!]${NC} Make sure you clicked 'START SERVER' in Dashboard"
fi
echo ""

# Check 3: Active connections
echo -e "${YELLOW}[3/6]${NC} Checking for active connections on port ${PORT}..."
CONNECTIONS=$(netstat -tn 2>/dev/null | grep ":${PORT}" | grep ESTABLISHED | wc -l)
if [ "$CONNECTIONS" -gt 0 ]; then
    echo -e "${GREEN}[✓]${NC} Found ${CONNECTIONS} active connection(s):"
    netstat -tn | grep ":${PORT}" | grep ESTABLISHED | while read line; do
        REMOTE_IP=$(echo $line | awk '{print $5}' | cut -d: -f1)
        echo -e "    ${GREEN}→${NC} ${REMOTE_IP}"
    done
else
    echo -e "${YELLOW}[!]${NC} No active connections found"
    echo -e "${YELLOW}[!]${NC} Make sure your payload is running on the target device"
fi
echo ""

# Check 4: Firewall
echo -e "${YELLOW}[4/6]${NC} Checking firewall status..."
if command -v ufw &> /dev/null; then
    if sudo ufw status | grep -q "Status: active"; then
        echo -e "${YELLOW}[!]${NC} UFW firewall is active"
        if sudo ufw status | grep -q "${PORT}"; then
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
        echo -e "${YELLOW}[!]${NC} Could not verify iptables rules"
    fi
fi
echo ""

# Check 5: Network interfaces
echo -e "${YELLOW}[5/6]${NC} Listing network interfaces and IPs..."
echo -e "${BLUE}[i]${NC} Your IP addresses:"
ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print "    " $2}' | cut -d/ -f1
echo ""

# Check 6: Test connection
echo -e "${YELLOW}[6/6]${NC} Testing local connection to port ${PORT}..."
if nc -zv localhost ${PORT} 2>&1 | grep -q "succeeded"; then
    echo -e "${GREEN}[✓]${NC} Local connection successful"
else
    echo -e "${RED}[✗]${NC} Local connection failed!"
    echo -e "${YELLOW}[!]${NC} The listener might not be properly started"
fi
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   📊 Diagnostic Summary                                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Recommendations
echo -e "${BLUE}[*]${NC} Recommendations:"
echo ""

if [ "$CONNECTIONS" -eq 0 ]; then
    echo -e "${YELLOW}[!]${NC} No active connections detected. To fix:"
    echo "   1. Make sure Dashboard is running"
    echo "   2. Click 'START SERVER' in Dashboard"
    echo "   3. On your phone, run the payload with:"
    YOUR_IP=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | head -1 | awk '{print $2}' | cut -d/ -f1)
    echo "      IP: ${YOUR_IP}"
    echo "      Port: ${PORT}"
    echo "   4. In Dashboard, click '🔍 SCAN' button"
    echo ""
fi

if pgrep -f "pentest_dashboard.py" > /dev/null; then
    echo -e "${GREEN}[✓]${NC} Dashboard is running - you can access it at:"
    echo "   http://localhost:5000"
    echo "   Password: hamza_sku_2026"
    echo ""
fi

echo -e "${BLUE}[*]${NC} Quick commands to try:"
echo "   View Dashboard logs:"
echo "   ${GREEN}tail -f dashboard.log${NC}"
echo ""
echo "   Check connections:"
echo "   ${GREEN}watch -n 1 'netstat -tn | grep :${PORT}'${NC}"
echo ""
echo "   Manual scan in Dashboard:"
echo "   ${GREEN}Click the '🔍 SCAN' button in Victims List${NC}"
echo ""

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Diagnostic Complete                                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
