# 🐉 أوامر مفيدة لـ Kali Linux

## 📋 أوامر التشغيل والإيقاف

### تشغيل Dashboard
```bash
# تشغيل عادي
python3 pentest_dashboard.py

# تشغيل في الخلفية
nohup python3 pentest_dashboard.py > dashboard.log 2>&1 &

# تشغيل باستخدام screen
screen -S pentest-c2
python3 pentest_dashboard.py
# اضغط Ctrl+A ثم D للخروج
```

### إيقاف Dashboard
```bash
# إيقاف عادي (في نفس Terminal)
Ctrl + C

# إيقاف من terminal آخر
pkill -f pentest_dashboard.py

# إيقاف قوي
sudo kill -9 $(pgrep -f pentest_dashboard.py)

# إيقاف المنفذ 5000
sudo lsof -ti:5000 | xargs kill -9
```

### العودة لـ Screen Session
```bash
# عرض جميع sessions
screen -ls

# العودة لـ session
screen -r pentest-c2

# إنهاء session
screen -X -S pentest-c2 quit
```

---

## 🔍 فحص حالة Dashboard

### التحقق من عمل Dashboard
```bash
# التحقق من العملية
ps aux | grep pentest_dashboard

# التحقق من المنفذ
netstat -tulpn | grep 5000
# أو
ss -tulpn | grep 5000

# التحقق من الاتصالات
lsof -i :5000
```

### مراقبة السجلات
```bash
# متابعة السجلات مباشرة
tail -f dashboard.log

# آخر 50 سطر
tail -n 50 dashboard.log

# بحث في السجلات
grep "ERROR" dashboard.log
grep "Login" dashboard.log
```

---

## 🌐 أوامر الشبكة

### معرفة IP الخاص بك
```bash
# IP الداخلي
ip addr show
# أو
hostname -I
# أو
ifconfig

# IP الخارجي
curl ifconfig.me
```

### فحص الاتصال
```bash
# فحص المنفذ من نفس الجهاز
curl http://localhost:5000

# فحص من الشبكة
curl http://192.168.1.X:5000

# فحص باستخدام netcat
nc -zv localhost 5000
```

### السماح بالاتصال عبر Firewall
```bash
# السماح بالمنفذ 5000
sudo ufw allow 5000

# التحقق من القواعد
sudo ufw status

# إعادة تحميل Firewall
sudo ufw reload

# تعطيل Firewall (للاختبار فقط)
sudo ufw disable
```

---

## 📦 إدارة المكتبات

### تثبيت المكتبات
```bash
# طريقة 1
pip3 install -r requirements.txt --break-system-packages

# طريقة 2 (باستخدام virtual environment)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# تثبيت مكتبة واحدة
pip3 install flask --break-system-packages
```

### تحديث المكتبات
```bash
# تحديث pip
pip3 install --upgrade pip

# تحديث مكتبة معينة
pip3 install --upgrade flask

# تحديث كل المكتبات
pip3 list --outdated
pip3 install --upgrade flask flask-socketio psutil
```

### التحقق من المكتبات المثبتة
```bash
# عرض جميع المكتبات
pip3 list

# التحقق من مكتبة معينة
pip3 show flask

# عرض dependencies
pip3 show flask | grep Requires
```

---

## 🔧 Git Commands (أوامر مفيدة)

### أوامر أساسية
```bash
# حالة المشروع
git status

# عرض التغييرات
git diff

# تاريخ commits
git log
git log --oneline
git log --graph --oneline --all

# عرض remote
git remote -v
```

### إضافة وحفظ تغييرات
```bash
# إضافة ملف واحد
git add filename.py

# إضافة كل الملفات
git add .

# إضافة ملفات معينة
git add *.py

# Commit
git commit -m "وصف التعديل"

# تعديل آخر commit
git commit --amend -m "وصف جديد"
```

### رفع وتحديث
```bash
# رفع على GitHub
git push origin main

# تحديث من GitHub
git pull origin main

# رفع فرع جديد
git push -u origin feature-branch
```

### إدارة الفروع
```bash
# إنشاء فرع جديد
git branch feature-new

# التبديل للفرع
git checkout feature-new

# إنشاء والتبديل
git checkout -b feature-new

# عرض جميع الفروع
git branch -a

# حذف فرع
git branch -d feature-name
```

### التراجع عن التغييرات
```bash
# التراجع عن تغييرات ملف
git checkout -- filename.py

# التراجع عن آخر commit (بدون حذف التغييرات)
git reset --soft HEAD~1

# التراجع عن آخر commit (مع حذف التغييرات)
git reset --hard HEAD~1

# إلغاء التغييرات والعودة لآخر commit
git reset --hard HEAD
```

---

## 🔍 أوامر فحص النظام

### استهلاك الموارد
```bash
# استهلاك CPU والذاكرة
htop
# أو
top

# استهلاك الذاكرة فقط
free -h

# مساحة القرص
df -h

# استهلاك مجلد معين
du -sh /path/to/folder
```

### العمليات الجارية
```bash
# جميع العمليات
ps aux

# عمليات Python
ps aux | grep python

# إيقاف عملية
kill PID
# أو قوي
kill -9 PID

# جميع عمليات المستخدم
ps -u $USER
```

---

## 🔒 أوامر الأمان

### فحص المنافذ المفتوحة
```bash
# جميع المنافذ
sudo netstat -tulpn

# منفذ معين
sudo netstat -tulpn | grep 5000

# باستخدام nmap
nmap localhost
nmap 192.168.1.X
```

### فحص الاتصالات النشطة
```bash
# جميع الاتصالات
netstat -an

# اتصالات ESTABLISHED
netstat -an | grep ESTABLISHED

# عدد الاتصالات لكل IP
netstat -an | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c
```

### تغيير صلاحيات الملفات
```bash
# قراءة وكتابة وتنفيذ للمالك فقط
chmod 700 pentest_dashboard.py

# قراءة وتنفيذ للجميع
chmod 755 setup.sh

# قراءة فقط
chmod 444 config.py

# إضافة صلاحية التنفيذ
chmod +x script.sh

# إزالة صلاحية الكتابة
chmod -w file.txt
```

---

## 📝 أوامر التحرير والبحث

### تحرير الملفات
```bash
# باستخدام nano
nano pentest_dashboard.py

# باستخدام vim
vim pentest_dashboard.py

# باستخدام gedit (GUI)
gedit pentest_dashboard.py &
```

### البحث في الملفات
```bash
# البحث عن نص في ملف
grep "MASTER_PASSWORD" pentest_dashboard.py

# البحث في جميع الملفات
grep -r "MASTER_PASSWORD" .

# البحث عن ملف
find . -name "*.py"

# البحث عن ملفات كبيرة
find . -type f -size +10M
```

### استبدال النصوص
```bash
# استبدال في ملف
sed -i 's/old_text/new_text/g' file.py

# استبدال في جميع الملفات
find . -name "*.py" -exec sed -i 's/old/new/g' {} +
```

---

## 🔄 النسخ الاحتياطي

### نسخ احتياطي للمشروع
```bash
# نسخ المجلد بالكامل
cp -r pentest-c2-dashboard pentest-c2-dashboard-backup

# أرشفة وضغط
tar -czf pentest-backup-$(date +%Y%m%d).tar.gz pentest-c2-dashboard/

# نسخ إلى USB
cp -r pentest-c2-dashboard /media/usb/

# مزامنة مع مجلد آخر
rsync -av pentest-c2-dashboard/ /backup/location/
```

### استعادة النسخة الاحتياطية
```bash
# فك الضغط
tar -xzf pentest-backup-20250126.tar.gz

# نسخ من backup
cp -r /backup/location/* .
```

---

## 🚀 تحسينات الأداء

### تنظيف الذاكرة
```bash
# مسح cache
sudo sync; echo 3 > /proc/sys/vm/drop_caches

# عرض استهلاك الذاكرة
free -h
```

### تنظيف المساحة
```bash
# حذف ملفات .pyc
find . -name "*.pyc" -delete

# حذف __pycache__
find . -name "__pycache__" -type d -exec rm -rf {} +

# حذف logs القديمة
find logs/ -name "*.log" -mtime +30 -delete

# تنظيف apt cache
sudo apt clean
sudo apt autoclean
```

---

## 🎯 Aliases مفيدة (اختصارات)

### إضافة اليوميات
```bash
# أضف في ~/.bashrc أو ~/.zshrc

# اختصارات Dashboard
alias pt-start='python3 ~/pentest-c2-dashboard/pentest_dashboard.py'
alias pt-stop='pkill -f pentest_dashboard.py'
alias pt-log='tail -f ~/pentest-c2-dashboard/dashboard.log'
alias pt-status='ps aux | grep pentest_dashboard'

# اختصارات Git
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push origin main'
alias gl='git log --oneline'

# اختصارات عامة
alias ll='ls -lah'
alias update='sudo apt update && sudo apt upgrade -y'
alias ip='ip addr show'

# ثم نفذ:
source ~/.bashrc
```

---

## 🔧 استكشاف الأخطاء

### خطأ: ModuleNotFoundError
```bash
# تثبيت المكتبة المفقودة
pip3 install module-name --break-system-packages
```

### خطأ: Permission denied
```bash
# إضافة صلاحيات
chmod +x filename
# أو استخدم sudo
sudo python3 pentest_dashboard.py
```

### خطأ: Port already in use
```bash
# إيقاف العملية على المنفذ
sudo lsof -ti:5000 | xargs kill -9
```

### خطأ: Cannot connect to GitHub
```bash
# التحقق من الاتصال
ping github.com

# إعادة ضبط remote
git remote remove origin
git remote add origin https://github.com/username/repo.git
```

---

## 💡 نصائح إضافية

### استخدام Screen بفعالية
```bash
# إنشاء session جديد
screen -S dashboard

# الخروج بدون إيقاف
Ctrl+A, D

# العودة
screen -r dashboard

# قائمة sessions
screen -ls

# إيقاف session
screen -X -S dashboard quit
```

### استخدام tmux (بديل لـ screen)
```bash
# تثبيت tmux
sudo apt install tmux

# إنشاء session
tmux new -s dashboard

# الخروج
Ctrl+B, D

# العودة
tmux attach -t dashboard
```

---

**احفظ هذا الملف كمرجع! 📌**
