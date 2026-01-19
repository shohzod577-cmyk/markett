# AWS EC2 ga Markett Django Ilovasini Joylash Qo'llanmasi

## 1. AWS EC2 Instance Yaratish

### 1.1. AWS Console ga kirish
- AWS Management Console ga kiring
- EC2 xizmatiga o'ting

### 1.2. Instance yaratish
1. **Launch Instance** tugmasini bosing
2. Quyidagi sozlamalarni tanlang:
   - **Name**: markett-production
   - **OS**: Ubuntu Server 22.04 LTS
   - **Instance type**: t3.medium yoki t3.large (traffic ga qarab)
   - **Key pair**: Yangi key pair yarating (.pem faylini saqlang!)
   - **Network settings**:
     - Allow SSH (port 22)
     - Allow HTTP (port 80)
     - Allow HTTPS (port 443)
   - **Storage**: 30 GB gp3 (minimal)

3. **Launch Instance** tugmasini bosing

### 1.3. Elastic IP qo'shish
1. EC2 Dashboard dan **Elastic IPs** ga o'ting
2. **Allocate Elastic IP address** ni bosing
3. Yaratilgan IP ni instancega biriktiring

## 2. Domen Sozlash (Opsional)

Agar domeningiz bo'lsa:
1. Domen provayderingizda A record yarating
2. A record ni Elastic IP ga yo'naltiring
3. Kutish vaqti: 5-60 daqiqa

## 3. Serverga Ulanish

```bash
# Windows PowerShell (yoki Git Bash)
ssh -i "markett-key.pem" ubuntu@your-elastic-ip

# Linux/Mac
chmod 400 markett-key.pem
ssh -i "markett-key.pem" ubuntu@your-elastic-ip
```

## 4. Loyihani Serverga Ko'chirish

### Variant 1: Git orqali (Tavsiya etiladi)

```bash
# Serverda
cd /home/ubuntu
git clone https://github.com/yourusername/markett.git
cd markett
```

### Variant 2: SCP orqali

```bash
# Windows PowerShell (local kompyuterda)
scp -i "markett-key.pem" -r "d:\shohzod 2025\Markett" ubuntu@your-elastic-ip:/home/ubuntu/markett
```

## 5. Server Setup

```bash
# Serverda
cd /home/ubuntu/markett
chmod +x deployment/setup_server.sh
./deployment/setup_server.sh
```

Bu skript quyidagilarni o'rnatadi:
- Python 3.11
- PostgreSQL client
- Redis
- Nginx
- Virtual environment
- Python packages
- Gunicorn service
- Celery service

## 6. Ma'lumotlar Bazasini Sozlash

### Variant A: AWS RDS PostgreSQL (Tavsiya etiladi)

1. **RDS Instance yaratish**:
   - AWS Console → RDS → Create database
   - Engine: PostgreSQL 15
   - Template: Free tier (test uchun) yoki Production
   - DB instance identifier: markett-db
   - Master username: markett_user
   - Master password: (kuchli parol yarating)
   - Instance type: db.t3.micro (free tier) yoki db.t3.small
   - Storage: 20 GB gp3
   - VPC: EC2 bilan bir xil
   - Public access: No
   - Security group: PostgreSQL (5432) dan EC2 security group ga ruxsat bering

2. **Database yaratish**:
```bash
# Serverda
sudo apt install postgresql-client -y
psql -h your-rds-endpoint.rds.amazonaws.com -U markett_user -d postgres
# Parolni kiriting
CREATE DATABASE markett_db;
\q
```

### Variant B: Local PostgreSQL

```bash
# Serverda
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -u postgres psql
CREATE DATABASE markett_db;
CREATE USER markett_user WITH PASSWORD 'your-strong-password';
GRANT ALL PRIVILEGES ON DATABASE markett_db TO markett_user;
ALTER USER markett_user CREATEDB;
\q
```

## 7. Environment Variables (.env) Sozlash

```bash
cd /home/ubuntu/markett
nano .env
```

`.env` faylini tahrirlang:
```bash
SECRET_KEY=your-secret-key-generate-with-django
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-elastic-ip

DB_ENGINE=django.db.backends.postgresql
DB_NAME=markett_db
DB_USER=markett_user
DB_PASSWORD=your-actual-password
DB_HOST=your-rds-endpoint.rds.amazonaws.com  # yoki localhost
DB_PORT=5432

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**SECRET_KEY yaratish:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 8. Domen va Nginx Sozlash

```bash
# Nginx config ni tahrirlash
sudo nano /etc/nginx/sites-available/markett
```

`your-domain.com` ni o'z domeningizga o'zgartiring

```bash
# Nginx tekshirish va restart
sudo nginx -t
sudo systemctl restart nginx
```

## 9. Django Migratsiyalar va Superuser

```bash
cd /home/ubuntu/markett
source venv/bin/activate

# Migratsiyalar
python manage.py migrate

# Static fayllar
python manage.py collectstatic --noinput

# Superuser yaratish
python manage.py createsuperuser
```

## 10. Servislarni Ishga Tushirish

```bash
# Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

# Celery
sudo systemctl start celery
sudo systemctl enable celery
sudo systemctl status celery

# Nginx
sudo systemctl restart nginx
sudo systemctl status nginx
```

## 11. SSL Sertifikat (Let's Encrypt)

```bash
# Certbot o'rnatish
sudo apt install certbot python3-certbot-nginx -y

# SSL sertifikat olish
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

## 12. Test Qilish

1. **Brauzerda ochish**: `http://your-domain.com` yoki `http://your-elastic-ip`
2. **Admin panel**: `http://your-domain.com/admin`
3. **API test**: Postman yoki curl bilan

## 13. Monitoring va Logs

```bash
# Gunicorn logs
tail -f /home/ubuntu/markett/logs/gunicorn-error.log
tail -f /home/ubuntu/markett/logs/gunicorn-access.log

# Celery logs
tail -f /home/ubuntu/markett/logs/celery.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Service status
sudo systemctl status gunicorn
sudo systemctl status celery
sudo systemctl status nginx
sudo systemctl status redis
```

## 14. Yangilashlar (Updates)

Keyinchalik kod o'zgarganda:

```bash
cd /home/ubuntu/markett
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

## 15. Xavfsizlik Sozlamalari

```bash
# Firewall
sudo ufw status
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Root loginni o'chirish
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no
sudo systemctl restart sshd

# Fail2ban o'rnatish
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## 16. Backup Sozlash

```bash
# Database backup script
nano /home/ubuntu/backup_db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump -h localhost -U markett_user markett_db > $BACKUP_DIR/db_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/ubuntu/markett/media/

# Old backuplarni o'chirish (30 kundan eski)
find $BACKUP_DIR -type f -mtime +30 -delete
```

```bash
chmod +x /home/ubuntu/backup_db.sh

# Crontab qo'shish (har kuni 2:00 da)
crontab -e
0 2 * * * /home/ubuntu/backup_db.sh
```

## 17. Performance Optimization

### Gunicorn Workers soni
```bash
# (2 x CPU cores) + 1
# t3.medium: 2 cores → 5 workers
sudo nano /etc/systemd/system/gunicorn.service
# --workers 5
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

### Redis cache qo'shish
`.env` ga qo'shing:
```
REDIS_URL=redis://localhost:6379/0
```

## 18. Troubleshooting

### Sayt ochilmayotgan bo'lsa:

```bash
# 1. Gunicorn ishlayaptimi?
sudo systemctl status gunicorn
sudo systemctl restart gunicorn

# 2. Nginx ishlayaptimi?
sudo systemctl status nginx
sudo nginx -t
sudo systemctl restart nginx

# 3. Loglarni tekshiring
tail -100 /home/ubuntu/markett/logs/gunicorn-error.log
sudo tail -100 /var/log/nginx/error.log

# 4. Port ochiqmi?
sudo netstat -tlnp | grep 8000
sudo netstat -tlnp | grep 80

# 5. Firewall sozlamalari
sudo ufw status
```

### Database connection error:

```bash
# PostgreSQL ishlayaptimi?
sudo systemctl status postgresql  # local uchun
# yoki
psql -h your-rds-endpoint -U markett_user -d markett_db  # RDS uchun

# .env fayl to'g'rimi?
cat /home/ubuntu/markett/.env | grep DB_
```

### Static files yuklanmayotgan bo'lsa:

```bash
cd /home/ubuntu/markett
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

## 19. Qo'shimcha Xizmatlar

### CloudWatch Monitoring (AWS)
- EC2 → Monitoring
- CloudWatch Alarms sozlash
- CPU, Memory, Disk usage monitoring

### S3 uchun Media Files (Opsional)
```bash
pip install boto3 django-storages
```

`settings.py` ga qo'shing:
```python
if config('USE_S3', default=False, cast=bool):
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

## 20. Xulosa

✅ EC2 instance yaratildi  
✅ Server sozlandi  
✅ PostgreSQL database sozlandi  
✅ Django ilova deploy qilindi  
✅ Nginx va Gunicorn ishga tushdi  
✅ SSL sertifikat o'rnatildi  
✅ Monitoring sozlandi  

**Saytingiz tayyor!** 🎉

Savollar bo'lsa yoki muammo bo'lsa, loglarni tekshiring va troubleshooting bo'limiga qarang.

---

## Foydali Komandalar

```bash
# Restart all services
sudo systemctl restart gunicorn celery nginx

# Check all services
sudo systemctl status gunicorn celery nginx redis

# View all logs
tail -f /home/ubuntu/markett/logs/*.log

# Django shell
cd /home/ubuntu/markett && source venv/bin/activate && python manage.py shell

# Clear cache
python manage.py clear_cache  # agar cache command bo'lsa
redis-cli FLUSHALL  # Redis cache uchun
```
