# AWS EC2 ga Markett Joylashtirish - Oddiy Qo'llanma
## (Git va Domensiz)

---

## 📋 KERAK BO'LADIGAN NARSALAR

- AWS Account
- Windows kompyuter
- Loyiha fayllari (d:\shohzod 2025\Markett)

---

## ⚡ TEZKOR QADAMLAR

### 1. AWS EC2 Instance Yaratish

#### a) AWS Console ga kiring
- https://console.aws.amazon.com
- **EC2** → **Launch Instance**

#### b) Sozlamalar:
```
Name: markett-server
Image: Ubuntu Server 22.04 LTS (Free tier eligible)
Instance type: t3.medium (yoki t2.medium)
Key pair: "Create new key pair" → Download markett-key.pem
```

#### c) Network Settings:
- ✅ Allow SSH traffic (port 22)
- ✅ Allow HTTP traffic (port 80)  
- ✅ Allow HTTPS traffic (port 443)

#### d) Storage: 30 GB

**Launch Instance!**

#### e) Elastic IP olish:
1. EC2 Dashboard → **Elastic IPs** → **Allocate Elastic IP**
2. Yaratilgan IP ni instance ga biriktiring (Associate)
3. IP ni yozib oling: `54.123.45.67` (masalan)

---

### 2. Key Faylni Tayyorlash

```powershell
# Downloads papkasiga o'ting
cd C:\Users\user\Downloads

# Ruxsatlarni sozlash (Windows)
icacls markett-key.pem /inheritance:r
icacls markett-key.pem /grant:r "%USERNAME%:R"
```

---

### 3. Serverga Ulanishni Test Qilish

```powershell
# Ulanishni tekshirish
ssh -i C:\Users\user\Downloads\markett-key.pem ubuntu@54.123.45.67
```

Agar ulanish bo'lsa, `exit` deb chiqing.

---

### 4. Loyihani Serverga Ko'chirish

```powershell
# PowerShell da
cd C:\Users\user\Downloads

# Butun loyihani yuborish (3-5 daqiqa)
scp -i markett-key.pem -r "d:\shohzod 2025\Markett" ubuntu@54.123.45.67:/home/ubuntu/
```

**Kutish:** Fayl hajmiga qarab 3-10 daqiqa.

---

### 5. Serverda Setup Qilish

```powershell
# Serverga ulanish
ssh -i C:\Users\user\Downloads\markett-key.pem ubuntu@54.123.45.67
```

Serverda:

```bash
# Papka nomini o'zgartirish
cd /home/ubuntu
mv Markett markett
cd markett

# Setup skriptni ishga tushirish
chmod +x deployment/setup_server.sh
./deployment/setup_server.sh
```

**Bu jarayon:** 5-10 daqiqa davom etadi. Python, Nginx, PostgreSQL o'rnatiladi.

---

### 6. .env Faylni Sozlash

```bash
# .env yaratish
cd /home/ubuntu/markett
cp deployment/.env.example .env
nano .env
```

**Minimal .env sozlamasi:**

```bash
# SECRET_KEY yaratish
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# .env faylda o'zgartirish
nano .env
```

`.env` da bu qatorlarni o'zgartiring:

```env
SECRET_KEY=<yuqoridagi SECRET_KEY ni joylashtiring>
DEBUG=False
ALLOWED_HOSTS=54.123.45.67  # <-- O'zingizning IP

# Database (local PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=markett_db
DB_USER=markett_user
DB_PASSWORD=kuchli_parol_123
DB_HOST=localhost
DB_PORT=5432

# Email (optional - konsolda chiqarish)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

`Ctrl+O` (saqlash), `Enter`, `Ctrl+X` (chiqish)

---

### 7. PostgreSQL Database Sozlash

```bash
# PostgreSQL o'rnatish
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql

# Database yaratish
sudo -u postgres psql << EOF
CREATE DATABASE markett_db;
CREATE USER markett_user WITH PASSWORD 'kuchli_parol_123';
GRANT ALL PRIVILEGES ON DATABASE markett_db TO markett_user;
ALTER USER markett_user CREATEDB;
\q
EOF
```

---

### 8. Django Setup

```bash
cd /home/ubuntu/markett
source venv/bin/activate

# Migrations
python manage.py migrate

# Static files
python manage.py collectstatic --noinput

# Superuser yaratish
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: <parol kiriting>
```

---

### 9. Servislarni Ishga Tushirish

```bash
# Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

# Celery
sudo systemctl start celery
sudo systemctl enable celery

# Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

### 10. ✅ TAYYOR! Test Qilish

Brauzeringizda:

```
http://54.123.45.67
```

Admin panel:
```
http://54.123.45.67/admin
```

---

## 🔧 MUAMMOLARNI HAL QILISH

### Sayt ochilmayotgan bo'lsa:

```bash
# 1. Servislarni tekshirish
sudo systemctl status gunicorn
sudo systemctl status nginx

# 2. Loglarni ko'rish
tail -f /home/ubuntu/markett/logs/gunicorn-error.log
sudo tail -f /var/log/nginx/error.log

# 3. Restart
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Database xatosi bo'lsa:

```bash
# PostgreSQL ishlayaptimi?
sudo systemctl status postgresql

# Database mavjudmi?
sudo -u postgres psql -c "\l"

# .env to'g'rimi?
cat /home/ubuntu/markett/.env | grep DB_
```

### Port ochilmaganmi?

```bash
# Firewall
sudo ufw status
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

## 🔄 YANGILASHLAR

Kodingizni o'zgartirgandan keyin:

```powershell
# Windows da (local)
scp -i C:\Users\user\Downloads\markett-key.pem -r "d:\shohzod 2025\Markett" ubuntu@54.123.45.67:/home/ubuntu/markett-new

# Serverda
ssh -i markett-key.pem ubuntu@54.123.45.67

# Serverda yangilash
cd /home/ubuntu
rm -rf markett/apps markett/static markett/templates
cp -r markett-new/Markett/* markett/
cd markett
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

**Yoki** deploy skript ishlatish:

```bash
cd /home/ubuntu/markett
./deployment/deploy.sh  # (agar git ishlatmasangiz, fayllarni avval SCP qiling)
```

---

## 📊 MONITORING

```bash
# Real-time logs
tail -f /home/ubuntu/markett/logs/gunicorn-error.log

# Service status
sudo systemctl status gunicorn nginx celery redis

# Disk space
df -h

# Memory
free -h
```

---

## 🔐 XAVFSIZLIK

```bash
# Firewall
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

# Fail2ban (optional)
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 💰 COST OPTIMIZATION

**t3.medium:** ~$30/oy  
**t2.micro (Free Tier):** $0 (12 oy)

Agar traffic kam bo'lsa:
- `t2.micro` yetarli
- Gunicorn workers: 2
- RDS o'rniga local PostgreSQL

---

## 📝 ESLATMALAR

1. ❌ **Domen kerak emas** - IP bilan ishlaydi
2. ❌ **Git kerak emas** - SCP bilan yuklaysiz
3. ❌ **SSL kerak emas** - HTTP yetarli (test uchun)
4. ✅ **IP o'zgarmasligi uchun Elastic IP ishlating**
5. ✅ **Backup qiling:** Database va media fayllar
6. ✅ **.env faylni hech qachon Git ga yuklmang!**

---

## ⚡ TEZKOR BACKUP

```bash
# Database backup
pg_dump -U markett_user markett_db > /home/ubuntu/backup_$(date +%Y%m%d).sql

# Media backup
tar -czf /home/ubuntu/media_backup.tar.gz /home/ubuntu/markett/media/
```

Download qilish:
```powershell
scp -i markett-key.pem ubuntu@54.123.45.67:/home/ubuntu/backup_*.sql C:\Users\user\Downloads\
```

---

## ✅ SUMMARY

1. EC2 instance yaratdingiz → ✅
2. Key file bilan ulandingiz → ✅  
3. SCP bilan fayllarni yukledingiz → ✅
4. Setup skript ishlatdingiz → ✅
5. .env sozladingiz → ✅
6. PostgreSQL yaratdingiz → ✅
7. Django migrations → ✅
8. Servislarni ishga tushirdingiz → ✅
9. IP da sayt ishlayapti → ✅

**Saytingiz tayyor!** 🎉

```
http://your-elastic-ip
```

---

## 📞 YORDAM KERAKMI?

Logs ni tekshiring:
```bash
tail -100 /home/ubuntu/markett/logs/gunicorn-error.log
```

Yoki servislarni restart qiling:
```bash
sudo systemctl restart gunicorn nginx
```
