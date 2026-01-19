# Markett E-commerce Platform

Django-based e-commerce platform with multi-language support, payment integrations, and modern features.

## Features

- 🛍️ Product catalog with categories and filters
- 🛒 Shopping cart and checkout
- 💳 Payment integrations (Click, Payme, Uzum)
- 👤 User authentication and profiles
- ⭐ Product reviews and ratings
- 📦 Order management
- 🌐 Multi-language support (Uzbek, Russian, English)
- 💱 Multi-currency support
- 📊 Dashboard analytics
- 📱 Responsive design

## Tech Stack

- **Framework**: Django 4.2.9
- **Database**: PostgreSQL / SQLite
- **Cache**: Redis
- **Task Queue**: Celery
- **Web Server**: Gunicorn + Nginx
- **Frontend**: Bootstrap 5, JavaScript
- **Deployment**: AWS EC2

## Quick Start (Development)

### Prerequisites
- Python 3.11+
- PostgreSQL (optional for development)
- Redis (optional for Celery)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd markett
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp deployment/.env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

8. Run development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Deployment to AWS

Complete deployment guide: [AWS_DEPLOYMENT_GUIDE.md](deployment/AWS_DEPLOYMENT_GUIDE.md)

### Quick Deployment Steps:

1. Create AWS EC2 instance (Ubuntu 22.04)
2. Copy project files to server
3. Run setup script:
```bash
chmod +x deployment/setup_server.sh
./deployment/setup_server.sh
```

4. Configure `.env` file
5. Setup SSL with Let's Encrypt
6. Done! 🎉

## Project Structure

```
markett/
├── apps/                  # Django applications
│   ├── cart/             # Shopping cart
│   ├── dashboard/        # Admin dashboard
│   ├── orders/           # Order management
│   ├── payments/         # Payment gateways
│   ├── products/         # Product catalog
│   ├── reviews/          # Reviews and ratings
│   └── users/            # User management
├── config/               # Project configuration
├── core/                 # Core utilities
├── deployment/           # Deployment configs
│   ├── nginx.conf
│   ├── gunicorn.service
│   ├── celery.service
│   ├── setup_server.sh
│   ├── deploy.sh
│   └── AWS_DEPLOYMENT_GUIDE.md
├── locale/               # Translations
├── media/                # User uploaded files
├── static/               # Static files
├── staticfiles/          # Collected static files
├── templates/            # HTML templates
├── manage.py
└── requirements.txt
```

## Configuration

### Environment Variables

Key environment variables (see `deployment/.env.example`):

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated hosts
- `DB_*`: Database configuration
- `EMAIL_*`: Email configuration
- `REDIS_URL`: Redis connection URL
- `*_MERCHANT_ID`, `*_SECRET_KEY`: Payment gateway credentials

### Database

Development (SQLite):
```env
DEBUG=True
# No DB_ENGINE needed - will use SQLite
```

Production (PostgreSQL):
```env
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=markett_db
DB_USER=markett_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Payment Gateways

Supported payment providers:
- Click
- Payme
- Uzum

Configure merchant credentials in `.env` file.

## Translation

Compile translation files:
```bash
python manage.py compilemessages
```

Update translations:
```bash
python manage.py makemessages -l uz
python manage.py makemessages -l ru
python manage.py compilemessages
```

## Testing

Run tests:
```bash
python manage.py test
```

## Maintenance

### Update Deployment
```bash
./deployment/deploy.sh
```

### View Logs
```bash
# Gunicorn
tail -f /home/ubuntu/markett/logs/gunicorn-error.log

# Celery
tail -f /home/ubuntu/markett/logs/celery.log

# Nginx
sudo tail -f /var/log/nginx/error.log
```

### Restart Services
```bash
sudo systemctl restart gunicorn
sudo systemctl restart celery
sudo systemctl restart nginx
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- GitHub Issues: <your-repo-url>/issues
- Email: your-email@example.com

## Acknowledgments

- Django Framework
- Bootstrap
- Payment Gateway Providers
- AWS

---

Made with ❤️ by Your Team
