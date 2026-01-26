# 🐉 دليل التشغيل على Kali Linux + رفع على GitHub

## 📋 المحتويات
1. [التشغيل على Kali Linux](#kali-setup)
2. [رفع المشروع على GitHub](#github-upload)
3. [حل المشاكل الشائعة](#troubleshooting)

---

## 🐉 الجزء الأول: التشغيل على Kali Linux {#kali-setup}

### الخطوة 1️⃣: تحديث النظام

```bash
# فتح Terminal
sudo apt update && sudo apt upgrade -y
```

### الخطوة 2️⃣: تثبيت المتطلبات الأساسية

```bash
# تثبيت Python 3 وpip (عادة مثبتة مسبقاً في Kali)
sudo apt install python3 python3-pip -y

# تثبيت git
sudo apt install git -y

# تثبيت netcat (مثبت مسبقاً عادة)
sudo apt install netcat-traditional -y
```

### الخطوة 3️⃣: إنشاء مجلد المشروع

```bash
# إنشاء مجلد في Home Directory
cd ~
mkdir pentest-c2-dashboard
cd pentest-c2-dashboard

# أو في مجلد مخصص
mkdir -p ~/Projects/pentest-c2-dashboard
cd ~/Projects/pentest-c2-dashboard
```

### الخطوة 4️⃣: نقل الملفات

```bash
# إذا كانت الملفات على USB أو مكان آخر
# انسخها للمجلد الحالي
cp /path/to/files/* .

# أو حمّل الملفات من الكمبيوتر الحالي إلى Kali
# استخدم scp أو USB أو الطرق المتاحة لديك
```

### الخطوة 5️⃣: تثبيت المكتبات المطلوبة

```bash
# طريقة 1: استخدام setup.sh
chmod +x setup.sh
./setup.sh

# طريقة 2: يدوياً
pip3 install -r requirements.txt --break-system-packages

# أو بدون --break-system-packages إذا واجهت مشكلة
pip3 install Flask flask-socketio python-socketio psutil werkzeug
```

### الخطوة 6️⃣: إعطاء صلاحيات التنفيذ

```bash
chmod +x pentest_dashboard.py
chmod +x setup.sh
```

### الخطوة 7️⃣: التشغيل!

```bash
# طريقة 1: مباشرة
python3 pentest_dashboard.py

# طريقة 2: في الخلفية
nohup python3 pentest_dashboard.py > dashboard.log 2>&1 &

# طريقة 3: باستخدام screen
screen -S pentest-c2
python3 pentest_dashboard.py
# اضغط Ctrl+A ثم D للخروج بدون إيقاف
```

### الخطوة 8️⃣: الوصول للـ Dashboard

```bash
# افتح Firefox أو أي متصفح في Kali
firefox http://localhost:5000

# أو من جهاز آخر في نفس الشبكة
# ابحث عن IP الخاص بـ Kali
ip addr show

# من جهاز آخر:
# http://KALI_IP:5000
# مثال: http://192.168.1.100:5000
```

### الخطوة 9️⃣: تسجيل الدخول

```
Password: hamza_sku_2026
```

### 🎉 مبروك! Dashboard شغال على Kali!

---

## 🚀 الجزء الثاني: رفع المشروع على GitHub {#github-upload}

### الخطوة 1️⃣: إنشاء حساب GitHub

```
1. اذهب إلى: https://github.com
2. اضغط "Sign up"
3. أكمل التسجيل
4. تحقق من البريد الإلكتروني
```

### الخطوة 2️⃣: إعداد Git على Kali

```bash
# إعداد اسمك وبريدك الإلكتروني
git config --global user.name "اسمك"
git config --global user.email "بريدك@example.com"

# مثال:
git config --global user.name "Hamza"
git config --global user.email "hamza@example.com"

# التحقق من الإعدادات
git config --list
```

### الخطوة 3️⃣: إنشاء Repository على GitHub

```
1. اذهب إلى: https://github.com
2. اضغط على زر "+" في الأعلى
3. اختر "New repository"
4. املأ البيانات:
   - Repository name: pentest-c2-dashboard
   - Description: Advanced PenTest C2 Dashboard with Authentication
   - Public أو Private (اختر Private للأمان)
   - ✅ لا تضف README (لأنه موجود مسبقاً)
5. اضغط "Create repository"
```

### الخطوة 4️⃣: إعداد المشروع للرفع

```bash
# التأكد من أنك في مجلد المشروع
cd ~/pentest-c2-dashboard

# إنشاء .gitignore لتجاهل الملفات غير المهمة
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.log

# Flask
instance/
.webassets-cache

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Custom
logs/
*.db
.env
EOF
```

### الخطوة 5️⃣: تهيئة Git Repository

```bash
# إنشاء repository محلي
git init

# إضافة جميع الملفات
git add .

# عمل أول commit
git commit -m "🚀 Initial commit: PenTest C2 Dashboard with authentication"
```

### الخطوة 6️⃣: ربط المشروع بـ GitHub

```bash
# استبدل USERNAME باسم مستخدم GitHub الخاص بك
git remote add origin https://github.com/USERNAME/pentest-c2-dashboard.git

# مثال:
# git remote add origin https://github.com/hamza-sku/pentest-c2-dashboard.git

# التحقق من الربط
git remote -v
```

### الخطوة 7️⃣: رفع المشروع على GitHub

```bash
# رفع الكود
git push -u origin main

# إذا طلب منك اسم المستخدم وكلمة المرور:
# Username: اسم مستخدم GitHub
# Password: استخدم Personal Access Token (ليس كلمة المرور العادية)
```

### 🔑 إنشاء Personal Access Token

إذا طلب منك Password:

```
1. اذهب إلى: https://github.com/settings/tokens
2. اضغط "Generate new token" > "Generate new token (classic)"
3. املأ:
   - Note: Kali Linux Token
   - Expiration: 90 days (أو حسب رغبتك)
   - ✅ repo (اختر جميع الخيارات تحتها)
4. اضغط "Generate token"
5. انسخ التوكن (لن تراه مرة أخرى!)
6. استخدمه كـ Password في git push
```

### الخطوة 8️⃣: ✅ تم الرفع بنجاح!

```
الآن المشروع موجود على:
https://github.com/USERNAME/pentest-c2-dashboard
```

---

## 🔄 تحديث المشروع على GitHub

### عند إضافة تعديلات جديدة:

```bash
# إضافة التعديلات
git add .

# عمل commit مع وصف التعديل
git commit -m "✨ Added new feature: XYZ"

# رفع التحديثات
git push origin main
```

### أمثلة على رسائل commit:

```bash
git commit -m "🐛 Fixed login bug"
git commit -m "✨ Added 2FA authentication"
git commit -m "📝 Updated documentation"
git commit -m "🎨 Improved UI design"
git commit -m "🔒 Enhanced security"
git commit -m "⚡ Performance improvements"
```

---

## 📥 تحميل المشروع من GitHub (Clone)

### على أي جهاز Kali آخر:

```bash
# تحميل المشروع
git clone https://github.com/USERNAME/pentest-c2-dashboard.git

# الدخول للمجلد
cd pentest-c2-dashboard

# التثبيت والتشغيل
./setup.sh
python3 pentest_dashboard.py
```

---

## 🛠️ حل المشاكل الشائعة {#troubleshooting}

### المشكلة 1: Permission denied

```bash
# الحل:
chmod +x setup.sh
chmod +x pentest_dashboard.py
```

### المشكلة 2: pip install يفشل

```bash
# الحل 1:
pip3 install --upgrade pip
pip3 install -r requirements.txt --break-system-packages

# الحل 2: استخدم virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### المشكلة 3: المنفذ 5000 مستخدم

```bash
# الحل 1: إيقاف العملية على المنفذ
sudo lsof -ti:5000 | xargs kill -9

# الحل 2: تغيير المنفذ في الكود
# في pentest_dashboard.py، آخر سطر:
# غيّر port=5000 إلى port=8080
```

### المشكلة 4: git push يطلب username/password باستمرار

```bash
# الحل: حفظ credentials
git config --global credential.helper store

# المرة القادمة لن يطلب منك
```

### المشكلة 5: خطأ "remote origin already exists"

```bash
# الحل: حذف origin القديم
git remote remove origin

# إضافة origin جديد
git remote add origin https://github.com/USERNAME/pentest-c2-dashboard.git
```

### المشكلة 6: لا يمكن الوصول من جهاز آخر

```bash
# الحل 1: تأكد من Firewall
sudo ufw allow 5000
sudo ufw reload

# الحل 2: تأكد من أن الخادم يعمل على 0.0.0.0
# في الكود:
# socketio.run(app, host='0.0.0.0', port=5000)

# الحل 3: تأكد من الشبكة
ping KALI_IP
```

---

## 🔒 نصائح أمنية للـ GitHub

### ⚠️ قبل الرفع على GitHub:

1. **لا ترفع كلمة المرور الحقيقية!**
```bash
# قبل الرفع، غيّر كلمة المرور في الكود إلى شيء عام:
MASTER_PASSWORD = "change_me_in_production"
```

2. **أضف ملف .env للأسرار:**
```bash
# في .env (سيتم تجاهله بواسطة .gitignore)
PENTEST_PASSWORD=hamza_sku_2026

# في الكود:
import os
from dotenv import load_dotenv
load_dotenv()
MASTER_PASSWORD = os.getenv('PENTEST_PASSWORD', 'default_password')
```

3. **استخدم Private Repository:**
```
عند إنشاء Repository على GitHub، اختر "Private"
```

4. **أضف تحذير في README:**
```markdown
⚠️ **WARNING**: This tool is for authorized penetration testing only!
```

---

## 📋 Checklist كامل

### ✅ على Kali Linux:
- [ ] تحديث النظام
- [ ] تثبيت Python و pip
- [ ] تثبيت git
- [ ] إنشاء مجلد المشروع
- [ ] نسخ الملفات
- [ ] تثبيت المكتبات
- [ ] إعطاء صلاحيات التنفيذ
- [ ] تشغيل Dashboard
- [ ] الوصول عبر المتصفح
- [ ] تسجيل دخول ناجح

### ✅ على GitHub:
- [ ] إنشاء حساب GitHub
- [ ] إعداد git config
- [ ] إنشاء repository جديد
- [ ] إنشاء .gitignore
- [ ] عمل git init
- [ ] عمل git add
- [ ] عمل git commit
- [ ] ربط remote origin
- [ ] رفع الكود (git push)
- [ ] التحقق من الرفع على GitHub

---

## 🎥 فيديو توضيحي (خطوات سريعة)

```bash
# كل شيء في 5 دقائق!

# 1. Setup
cd ~ && mkdir pentest-c2-dashboard && cd pentest-c2-dashboard
# ضع الملفات هنا
pip3 install -r requirements.txt --break-system-packages

# 2. Test
python3 pentest_dashboard.py
# افتح firefox localhost:5000

# 3. Git Init
git init
cat > .gitignore << 'EOF'
__pycache__/
*.log
.env
EOF
git add .
git commit -m "🚀 Initial commit"

# 4. Push to GitHub
git remote add origin https://github.com/USERNAME/pentest-c2-dashboard.git
git push -u origin main

# ✅ Done!
```

---

## 📞 دعم إضافي

### موارد مفيدة:
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com)
- [Kali Linux Docs](https://www.kali.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com)

### أوامر Git المفيدة:
```bash
git status          # حالة المشروع
git log             # تاريخ commits
git diff            # التغييرات
git branch          # الفروع
git pull            # تحديث من GitHub
```

---

## 🎯 الخلاصة

### أنت الآن تعرف:
1. ✅ كيف تشغل Dashboard على Kali Linux
2. ✅ كيف ترفع المشروع على GitHub
3. ✅ كيف تحدث المشروع
4. ✅ كيف تحل المشاكل الشائعة

---

**مبروك! 🎉 أنت الآن محترف في Git و Kali Linux! 🐉**

*Happy Hacking (Ethically)!* 🔒
