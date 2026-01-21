# 🚀 Markett - AWS Elastic Beanstalk Deployment Guide

Bu qo'llanma Markett loyihasini AWS Elastic Beanstalk orqali deploy qilish jarayonini tushuntiradi.

## 📋 Bo'limlar

1. [Talablar](#talablar)
2. [AWS Sozlamalari](#aws-sozlamalari)
3. [Elastic Beanstalk Application Yaratish](#elastic-beanstalk-application-yaratish)
4. [Deploy Qilish](#deploy-qilish)
5. [Database Sozlash (RDS)](#database-sozlash-rds)
6. [Redis/Celery Sozlash (ElastiCache)](#redis-celery-sozlash-elasticache)
7. [S3 Media Storage Sozlash](#s3-media-storage-sozlash)
8. [Environment Variables](#environment-variables)
9. [Muammolarni Hal Qilish](#muammolarni-hal-qilish)

---

## ✅ Talablar

### 1. AWS Account
- AWS account yarating: https://aws.amazon.com
- Billing sozlamalarini tekshiring

### 2. EB CLI O'rnatish

```bash
# Python orqali
pip install awsebcli

# Tekshirish
eb --version
```

### 3. AWS Credentials Sozlash

```bash
# AWS CLI o'rnatish (agar yo'q bo'lsa)
pip install awscli

# AWS credentials sozlash
aws configure
```

Quyidagilarni kiriting:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `eu-north-1` (Stockholm)
- Default output format: `json`

---

## 🔧 AWS Sozlamalari

### 1. IAM User Yaratish

1. AWS Console → IAM → Users → Add user
2. User name: `markett-deploy`
3. Access type: Programmatic access
4. Permissions: `AdministratorAccess-AWSElasticBeanstalk`
5. Access Key ID va Secret ni saqlang

### 2. Region Tanlash

Tavsiya etiladi: **Europe (Stockholm) - eu-north-1**

Sabablari:
- Eng yaqin geografik joylashuv
- Past latency
- GDPR compliance

---

## 📦 Elastic Beanstalk Application Yaratish

### Variant 1: AWS Console Orqali (Vizual)

1. **AWS Console ga kirish**
   - https://console.aws.amazon.com
   - Elastic Beanstalk xizmatiga o'ting
   - Region: `Europe (Stockholm) eu-north-1`

2. **Create Application**
   - Application name: `Markett`
   - Platform: `Python 3.11 on Amazon Linux 2023`
   - Platform branch: Latest
   - Platform version: Latest recommended

3. **Application code**
   - Sample application (keyinroq deploy qilamiz)
   - yoki Upload your code (ZIP fayl)

4. **Configure more options** (Advanced settings)
   
   **Software:**
   - WSGI path: `config.wsgi:application`
   - Environment variables: (keyinroq qo'shamiz)
   
   **Instances:**
   - Instance type: `t3.small` (minimal) yoki `t3.medium` (tavsiya)
   
   **Capacity:**
   - Environment type: `Load balanced` (production uchun)
   - Instances: Min 1, Max 4
   - yoki Single instance (test uchun)
   
   **Load balancer:**
   - Type: Application Load Balancer
   - Listener: HTTP 80, HTTPS 443 (SSL sertifikat qo'shing)
   
   **Security:**
   - EC2 key pair: Yangi key pair yarating (SSH uchun)

5. **Create environment**
   - Environment name: `markett-production`
   - Domain: `markett-production` (yoki o'zingizniki)

### Variant 2: EB CLI Orqali (Terminal)

```bash
# Loyiha papkasiga o'ting
cd "d:\shohzod 2025\Markett"

# EB init - Application yaratish
eb init

# Quyidagilarni tanlang:
# - Region: 18) eu-north-1 : Europe (Stockholm)
# - Application name: Markett
# - Platform: Python 3.11
# - SSH: Yes (key pair yarating)

# Environment yaratish
eb create markett-production

# yoki custom settings bilan
eb create markett-production \
  --instance-type t3.medium \
  --envvars DEBUG=False,DJANGO_SETTINGS_MODULE=config.settings
```

---

## 🚀 Deploy Qilish

### Birinchi Deploy

```bash
# 1. Virtual environment yarating (local test uchun)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Dependencies o'rnatish
pip install -r requirements.txt

# 3. Static files yig'ish
python manage.py collectstatic --noinput

# 4. Migrations tekshirish
python manage.py showmigrations

# 5. Deploy qilish
eb deploy markett-production
```

### Deploy Script Bilan

```bash
# eb-deploy.sh scriptidan foydalanish
chmod +x eb-deploy.sh  # Linux/Mac
./eb-deploy.sh markett-production

# Windows PowerShell
bash eb-deploy.sh markett-production
```

### Deploy Status Tekshirish

```bash
# Environment status
eb status

# Logs ko'rish
eb logs

# Real-time logs
eb logs --stream

# Application ochish
eb open
```

---

## 🗄️ Database Sozlash (RDS)

### 1. RDS PostgreSQL Yaratish

**AWS Console → RDS → Create database:**

- **Engine:** PostgreSQL 15
- **Template:** Production (yoki Free tier test uchun)
- **DB instance identifier:** `markett-db`
- **Master username:** `markett_user`
- **Master password:** (kuchli parol yarating va saqlang)
- **DB instance class:**
  - `db.t3.micro` (Free tier - test)
  - `db.t3.small` (Production)
- **Storage:**
  - Type: gp3
  - Allocated: 20 GB
  - Enable autoscaling: 100 GB max
- **Connectivity:**
  - VPC: Elastic Beanstalk bilan bir xil
  - Public access: No
  - VPC security group: Yangi yarating `markett-db-sg`
- **Database authentication:** Password authentication
- **Initial database name:** `markett_db`

### 2. Security Group Sozlash

1. **RDS Security Group** (`markett-db-sg`):
   - Inbound rules qo'shing
   - Type: PostgreSQL
   - Port: 5432
   - Source: EB environment security group

2. **EB Environment ga RDS Ulash:**

```bash
# EB console orqali environment variables qo'shing
eb setenv \
  DB_NAME=markett_db \
  DB_USER=markett_user \
  DB_PASSWORD=your-password \
  DB_HOST=markett-db.xxxxx.eu-north-1.rds.amazonaws.com \
  DB_PORT=5432
```

### 3. Migrations Run Qilish

```bash
# SSH orqali instance ga kirish
eb ssh markett-production

# Migrations
cd /var/app/current
source /var/app/venv/*/bin/activate
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Exit
exit
```

---

## 🔄 Redis/Celery Sozlash (ElastiCache)

### 1. ElastiCache Redis Yaratish

**AWS Console → ElastiCache → Redis → Create:**

- **Cluster name:** `markett-redis`
- **Engine version:** 7.0
- **Node type:** `cache.t3.micro` (test) yoki `cache.t3.small`
- **Number of replicas:** 1 (production uchun)
- **Subnet group:** EB bilan bir xil VPC
- **Security group:** Yangi yarating `markett-redis-sg`

### 2. Security Group

**markett-redis-sg Inbound rules:**
- Type: Custom TCP
- Port: 6379
- Source: EB environment security group

### 3. Environment Variables

```bash
eb setenv \
  REDIS_URL=redis://markett-redis.xxxxx.cache.amazonaws.com:6379/0 \
  CELERY_BROKER_URL=redis://markett-redis.xxxxx.cache.amazonaws.com:6379/0 \
  CELERY_RESULT_BACKEND=redis://markett-redis.xxxxx.cache.amazonaws.com:6379/0
```

### 4. Celery Worker Sozlash

`.ebextensions/02_celery.config` yarating:

```yaml
files:
  "/opt/elasticbeanstalk/tasks/taillogs.d/celery.conf":
    mode: "000644"
    owner: root
    group: root
    content: |
      /var/log/celery-worker.log

container_commands:
  01_celery_worker:
    command: "source /var/app/venv/*/bin/activate && celery -A config worker -l info --detach --logfile=/var/log/celery-worker.log"
    leader_only: true
  02_celery_beat:
    command: "source /var/app/venv/*/bin/activate && celery -A config beat -l info --detach --logfile=/var/log/celery-beat.log"
    leader_only: true
```

---

## 📁 S3 Media Storage Sozlash

### 1. S3 Bucket Yaratish

```bash
# AWS CLI orqali
aws s3 mb s3://markett-media --region eu-north-1

# Public access blokirovka qilish
aws s3api put-public-access-block \
  --bucket markett-media \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### 2. CORS Sozlash

`cors.json` yarating:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag"]
    }
]
```

```bash
aws s3api put-bucket-cors \
  --bucket markett-media \
  --cors-configuration file://cors.json
```

### 3. IAM Policy Yaratish

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::markett-media",
                "arn:aws:s3:::markett-media/*"
            ]
        }
    ]
}
```

### 4. Environment Variables

```bash
eb setenv \
  USE_S3=True \
  AWS_STORAGE_BUCKET_NAME=markett-media \
  AWS_S3_REGION_NAME=eu-north-1
```

### 5. Django Settings

`config/settings.py` da S3 sozlamalari allaqachon mavjud:

```python
if config('USE_S3', default=False, cast=bool):
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='eu-north-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
```

---

## 🔐 Environment Variables

### Barcha Kerakli Environment Variables

```bash
# Django Core
eb setenv SECRET_KEY=your-super-secret-key-change-this
eb setenv DEBUG=False
eb setenv ALLOWED_HOSTS=.elasticbeanstalk.com,.yourdomain.com

# Database
eb setenv DB_NAME=markett_db
eb setenv DB_USER=markett_user
eb setenv DB_PASSWORD=your-db-password
eb setenv DB_HOST=markett-db.xxxxx.eu-north-1.rds.amazonaws.com
eb setenv DB_PORT=5432

# Redis
eb setenv REDIS_URL=redis://markett-redis.xxxxx.cache.amazonaws.com:6379/0
eb setenv CELERY_BROKER_URL=redis://markett-redis.xxxxx.cache.amazonaws.com:6379/0

# S3
eb setenv USE_S3=True
eb setenv AWS_STORAGE_BUCKET_NAME=markett-media
eb setenv AWS_S3_REGION_NAME=eu-north-1

# Email
eb setenv EMAIL_HOST=smtp.gmail.com
eb setenv EMAIL_PORT=587
eb setenv EMAIL_USE_TLS=True
eb setenv EMAIL_HOST_USER=your-email@gmail.com
eb setenv EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateways
eb setenv PAYME_MERCHANT_ID=your-payme-id
eb setenv PAYME_SECRET_KEY=your-payme-secret
eb setenv CLICK_MERCHANT_ID=your-click-id
eb setenv CLICK_SECRET_KEY=your-click-secret
```

### AWS Console Orqali

1. EB Environment → Configuration → Software → Environment properties
2. Har bir variable ni qo'shing
3. Apply

---

## 🌐 Custom Domain Sozlash

### 1. Domain Provider da

A record yarating:
- Name: `@` (yoki subdomain)
- Value: EB environment URL yoki Load Balancer IP
- TTL: 300

CNAME record:
- Name: `www`
- Value: `markett-production.eu-north-1.elasticbeanstalk.com`

### 2. SSL Sertifikat (HTTPS)

**AWS Certificate Manager:**

1. ACM → Request certificate
2. Domain: `yourdomain.com` va `*.yourdomain.com`
3. Validation: DNS
4. Domain provider da CNAME records qo'shing

**EB Load Balancer ga SSL qo'shish:**

1. EB → Configuration → Load balancer
2. Add listener
3. Port: 443
4. Protocol: HTTPS
5. SSL certificate: ACM dan tanlang

### 3. ALLOWED_HOSTS Yangilash

```bash
eb setenv ALLOWED_HOSTS=.elasticbeanstalk.com,yourdomain.com,www.yourdomain.com
```

---

## 📊 Monitoring va Logs

### Logs Ko'rish

```bash
# Oxirgi loglar
eb logs

# Real-time streaming
eb logs --stream

# Specific log file
eb logs --log-group /aws/elasticbeanstalk/markett-production/var/log/web.stdout.log
```

### CloudWatch

1. AWS Console → CloudWatch → Logs
2. Log groups: `/aws/elasticbeanstalk/markett-production`
3. Metrics: CPU, Memory, Request count, Response time

### Health Monitoring

```bash
# Environment health
eb health

# Detailed health
eb health --refresh
```

---

## 🔧 Muammolarni Hal Qilish

### 1. Deploy Xatolar

```bash
# Detailed logs
eb logs --all

# SSH bilan kirish
eb ssh

# Application logs
cd /var/app/current
cat /var/log/eb-engine.log
cat /var/log/web.stdout.log
```

### 2. Database Connection Error

- Security group tekshiring
- DB credentials to'g'riligini tekshiring
- VPC va subnet sozlamalarini tekshiring

```bash
# SSH orqali test
eb ssh
ping markett-db.xxxxx.rds.amazonaws.com
telnet markett-db.xxxxx.rds.amazonaws.com 5432
```

### 3. Static Files Yulanmagan

```bash
# Collectstatic qayta run qiling
python manage.py collectstatic --noinput --clear

# Deploy
eb deploy
```

### 4. 502 Bad Gateway

- WSGI path tekshiring: `config.wsgi:application`
- Python version mos kelishini tekshiring
- Requirements.txt dependencies to'liqligini tekshiring

### 5. Memory Issues

- Instance type oshiring (t3.small → t3.medium)
- Gunicorn workers sonini kamaytiring
- Database connection pooling sozlang

---

## 🎯 Production Best Practices

### 1. Auto Scaling

```bash
# EB Console → Configuration → Capacity
- Environment type: Load balanced
- Min instances: 2
- Max instances: 4
- Scaling trigger: CPU > 70%
```

### 2. Backups

**RDS Automated Backups:**
- Retention period: 7 days
- Backup window: 03:00-04:00 UTC

**Manual Snapshots:**
```bash
aws rds create-db-snapshot \
  --db-instance-identifier markett-db \
  --db-snapshot-identifier markett-db-snapshot-$(date +%Y%m%d)
```

### 3. Security

- SSH key pairni xavfsiz saqlang
- Environment variables ni encrypt qiling
- Security groups minimal permissions qiling
- WAF (Web Application Firewall) qo'shing
- Regular security updates

### 4. Cost Optimization

- Reserved Instances (1-3 years)
- Auto Scaling policies
- S3 lifecycle policies
- RDS Reserved Instances
- CloudWatch alarms sozlang

---

## 📞 Qo'shimcha Resurslar

- **AWS EB Documentation:** https://docs.aws.amazon.com/elasticbeanstalk/
- **Django Deployment:** https://docs.djangoproject.com/en/4.2/howto/deployment/
- **AWS Free Tier:** https://aws.amazon.com/free/

---

## ✅ Deploy Checklist

Pre-deployment:
- [ ] AWS account va billing sozlangan
- [ ] EB CLI o'rnatilgan
- [ ] AWS credentials sozlangan
- [ ] .env fayl to'ldirilgan
- [ ] RDS database yaratilgan
- [ ] ElastiCache Redis yaratilgan
- [ ] S3 bucket yaratilgan
- [ ] Security groups sozlangan

Deployment:
- [ ] EB application yaratilgan
- [ ] Environment yaratilgan
- [ ] Environment variables sozlangan
- [ ] Code deploy qilingan
- [ ] Migrations run qilingan
- [ ] Superuser yaratilgan
- [ ] Static files yuklangan

Post-deployment:
- [ ] Application ochiladi (eb open)
- [ ] Admin panel ishlaydi
- [ ] Database ulanishi ishlaydi
- [ ] Media uploads ishlaydi
- [ ] Celery tasks ishlaydi
- [ ] SSL sertifikat sozlangan
- [ ] Custom domain sozlangan
- [ ] Monitoring va alertlar sozlangan
- [ ] Backup policies sozlangan

---

## 🎉 Deploy Tayyor!

Muvaffaqiyatli deploy bo'lsin! Savollar bo'lsa, [Issues](https://github.com/yourusername/markett/issues) da yozishingiz mumkin.
