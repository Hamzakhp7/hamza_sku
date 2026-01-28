# استكشاف الأخطاء - دليل عملي

## المشكلة الحقيقية في معظم الحالات:

### ❌ المكتبات غير مثبتة

إذا رأيت:
```
ModuleNotFoundError: No module named 'flask_socketio'
```

**الحل الفوري:**
```bash
pip3 install --user flask-socketio python-socketio Flask pymetasploit3 requests werkzeug
```

---

## خطوات الاختبار الحقيقية:

### 1. اختبر وجود المكتبات:
```bash
python3 << 'EOF'
try:
    import flask
    import flask_socketio
    import pymetasploit3
    import requests
    print("✓ جميع المكتبات موجودة")
except ImportError as e:
    print(f"✗ مكتبة ناقصة: {e}")
EOF
```

### 2. اختبر Metasploit RPC:
```bash
# شغّل msfrpcd أولاً
msfrpcd -P msf_password -S -a 127.0.0.1

# في terminal آخر، اختبر الاتصال:
python3 << 'EOF'
from pymetasploit3.msfrpc import MsfRpcClient
try:
    client = MsfRpcClient('msf_password', server='127.0.0.1', port=55553, ssl=False)
    print(f"✓ متصل بـ Metasploit: {client.core.version()}")
except Exception as e:
    print(f"✗ فشل الاتصال: {e}")
EOF
```

### 3. اختبر تشغيل Dashboard:
```bash
cd hamza_sku_metasploit_c2
python3 c2_server.py
```

**يجب أن ترى:**
```
╔═══════════════════════════════════════════════════════════╗
║            🔥 HAMZA SKU - C2 DASHBOARD 🔥                 ║
╚═══════════════════════════════════════════════════════════╝

📍 Dashboard URL: http://localhost:5000
✅ Server starting...

 * Running on http://127.0.0.1:5000
```

**إذا لم تر هذا، هناك خطأ حقيقي.**

### 4. اختبر Login:
```bash
# بعد تشغيل Dashboard، في terminal آخر:
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"password":"hamza_sku_2026"}'
```

**يجب أن ترى:**
```json
{"success":true}
```

---

## الأخطاء الشائعة والحلول:

### خطأ 1: `ModuleNotFoundError`
**السبب:** المكتبات غير مثبتة
**الحل:**
```bash
pip3 install --user flask-socketio python-socketio Flask pymetasploit3 requests werkzeug
```

### خطأ 2: `Address already in use`
**السبب:** المنفذ 5000 مستخدم
**الحل:**
```bash
# ابحث عن العملية:
lsof -i :5000
# أو:
netstat -tulpn | grep 5000

# أوقف العملية:
kill -9 <PID>
```

### خطأ 3: `Connection refused` عند الاتصال بـ Metasploit
**السبب:** msfrpcd غير شغال
**الحل:**
```bash
# تأكد من تشغيل msfrpcd:
ps aux | grep msfrpcd

# إذا لم يكن شغال، شغّله:
msfrpcd -P msf_password -S -a 127.0.0.1

# تأكد من المنفذ:
netstat -tulpn | grep 55553
```

### خطأ 4: Login لا يعمل
**السبب المحتمل:** المتصفح يخزن كلمة مرور خاطئة
**الحل:**
```bash
# 1. افتح Developer Tools (F12)
# 2. اذهب لـ Console
# 3. اكتب:
localStorage.clear();
sessionStorage.clear();
# 4. أعد تحميل الصفحة (Ctrl+R)
```

### خطأ 5: Dashboard يبدأ لكن لا يفتح في المتصفح
**التحقق:**
```bash
# اختبر الاتصال:
curl http://localhost:5000

# يجب أن ترى HTML
```

**إذا رأيت `Connection refused`:**
- Dashboard غير شغال فعلياً
- تحقق من logs في terminal

---

## الاختبار النهائي الشامل:

```bash
#!/bin/bash

echo "=== اختبار شامل ==="

# 1. Python
echo "1. Testing Python..."
python3 --version || echo "ERROR: Python not found"

# 2. المكتبات
echo "2. Testing libraries..."
python3 -c "import flask, flask_socketio, pymetasploit3, requests" 2>&1 && echo "✓ Libraries OK" || echo "✗ Libraries missing"

# 3. msfrpcd
echo "3. Testing msfrpcd..."
nc -zv 127.0.0.1 55553 2>&1 | grep succeeded && echo "✓ msfrpcd running" || echo "✗ msfrpcd not running"

# 4. Dashboard
echo "4. Testing Dashboard..."
curl -s http://localhost:5000 > /dev/null && echo "✓ Dashboard running" || echo "✗ Dashboard not running"

# 5. Login API
echo "5. Testing Login..."
RESPONSE=$(curl -s -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"password":"hamza_sku_2026"}')
echo $RESPONSE | grep -q '"success":true' && echo "✓ Login works" || echo "✗ Login failed"

echo "=== اختبار انتهى ==="
```

احفظ هذا في ملف `test.sh` وشغّله:
```bash
chmod +x test.sh
./test.sh
```

---

## المتطلبات الأساسية التي يجب توفرها:

1. **Python 3.8+** ✓
2. **pip3** ✓
3. **Metasploit Framework** ✓
4. **المكتبات المطلوبة:**
   - Flask
   - flask-socketio
   - python-socketio
   - pymetasploit3
   - requests
   - werkzeug

---

## إذا لم يعمل بعد كل هذا:

أعطني الـ **output الفعلي** من:

```bash
# 1. نسخة Python
python3 --version

# 2. محاولة تشغيل Dashboard
python3 c2_server.py 2>&1 | head -20

# 3. محاولة استيراد المكتبات
python3 -c "import flask, flask_socketio, pymetasploit3, requests" 2>&1

# 4. حالة msfrpcd
ps aux | grep msfrpcd

# 5. المنافذ المفتوحة
netstat -tulpn | grep -E "5000|55553"
```

أعطني هذا الـ output وسأعطيك الحل الدقيق.
