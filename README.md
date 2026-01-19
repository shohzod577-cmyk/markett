# 🚀 MARKET - Enterprise E-Commerce Platform

<div align="center">

![Market Logo](static/images/logo.png)

**Production-Grade E-Commerce System for Central Asian Market**

[![Django](https://img.shields.io/badge/Django-4.2.9-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [Payment Integration](#-payment-integration)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Security](#-security)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

**Market** is a production-ready, enterprise-grade e-commerce platform designed specifically for the Central Asian market (Uzbekistan-first). Built with Django and following industry best practices, it demonstrates senior-level software engineering skills suitable for academic defense and real-world deployment.

### Key Highlights

✅ **Clean Architecture** - Service layer, selectors, fat models, thin views  
✅ **Multi-Currency Support** - UZS, USD, EUR with real-time conversion  
✅ **Payment Gateways** - Click, Payme, Uzum Bank, Cash on Delivery  
✅ **Order Management** - Full lifecycle with state machine pattern  
✅ **Custom Admin Dashboard** - Professional analytics and management  
✅ **Review System** - Verified buyer reviews with anti-fraud measures  
✅ **PDF Generation** - Professional invoice system  
✅ **Email Notifications** - Transactional emails with templates  
✅ **Security First** - CSRF protection, input validation, secure payments  

---

## 🌟 Features

### 🛍️ **Customer Features**

#### Authentication & Profile
- User registration with email verification
- Secure login/logout with session management
- Profile management with avatar upload
- Multiple delivery addresses with geolocation
- Order history tracking

#### Product Discovery
- Advanced search with filters
- Category-based navigation
- Price range filtering
- Sort by:  newest, price, popularity, rating
- Product variants (size, color, etc.)
- Multi-image support per product
- Real-time stock availability

#### Shopping Experience
- Persistent shopping cart
- Multi-currency pricing (UZS, USD, EUR)
- Real-time price conversion
- Quantity management
- Cart summary with delivery estimates

#### Checkout Process
- Multi-step checkout flow
- Saved address selection
- Google Maps location picker
- Multiple payment methods: 
  - Cash on Delivery
  - Credit/Debit Card
  - Click Payment
  - Payme Payment
  - Uzum Bank
- Order notes and special instructions

#### Order Management
- Real-time order tracking
- Order status updates: 
  - Pending → Accepted → Packed → On the Way → Delivered
- Cancel orders (before shipment)
- Download PDF invoices
- Email notifications at each stage

#### Reviews & Ratings
- 5-star rating system
- Text reviews with images
- Verified purchase badges
- Helpful/Not Helpful voting
- Review moderation

---

### 👨‍💼 **Admin Features**

#### Custom Dashboard (NO Django Default Admin)
- Real-time analytics and metrics
- Revenue tracking by currency
- Order statistics with charts
- User growth analytics
- Top-selling products
- Low stock alerts

#### Order Management
- View all orders with filtering
- Update order status
- View order details and history
- Manage cancellations
- Track payments
- Generate reports

#### Product Management
- CRUD operations for products
- Category management
- Inventory tracking
- Bulk operations
- Stock alerts
- Sales analytics

#### User Management
- View user profiles
- Block/unblock users
- View purchase history
- Track customer behavior
- Export user data

#### Review Moderation
- Approve/reject reviews
- Flag inappropriate content
- Respond to reviews
- Analytics on review trends

---

## 🛠 Technology Stack

### Backend
- **Django 4.2.9** - Web framework
- **Python 3.10+** - Programming language
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Redis** - Caching & Celery broker

### Frontend
- **Bootstrap 5.3** - CSS framework
- **JavaScript/jQuery** - Interactivity
- **Chart.js** - Analytics charts
- **Google Maps API** - Location services

### Payment Integration
- **Click API** - Uzbekistan payment gateway
- **Payme API** - Uzbekistan payment gateway
- **Uzum Bank API** - Digital banking

### Additional Libraries
- **Pillow** - Image processing
- **ReportLab/WeasyPrint** - PDF generation
- **django-crispy-forms** - Form rendering
- **django-filter** - Advanced filtering
- **Celery** - Asynchronous tasks
- **Gunicorn** - WSGI HTTP server
- **WhiteNoise** - Static file serving

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Customer   │  │    Admin     │  │   Payment    │     │
│  │   Frontend   │  │  Dashboard   │  │   Webhooks   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Views     │  │   Services   │  │   Selectors  │     │
│  │  (Thin)      │  │  (Business   │  │  (Queries)   │     │
│  │              │  │   Logic)     │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────┐
│                         DOMAIN LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Models    │  │State Machines│  │  Validators  │     │
│  │   (Fat)      │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │    Redis     │  │   Payment    │     │
│  │   Database   │  │    Cache     │  │   Gateways   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns Used

1. **Service Layer Pattern** - Business logic isolation
2. **Repository Pattern** - Data access abstraction
3. **State Machine Pattern** - Order lifecycle management
4. **Strategy Pattern** - Payment gateway abstraction
5. **Factory Pattern** - Object creation
6. **Observer Pattern** - Event notifications

---

## 📦 Installation Guide

### Prerequisites

```bash
- Python 3.10 or higher
- pip (Python package manager)
- virtualenv or venv
- PostgreSQL 13+ (for production)
- Redis (for Celery)
- Git
```

### Step 1: Clone Repository

```bash
git clone https://github.com/TilovovSherzod/market.git
cd market
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configuration
nano .env  # or use any text editor
```

### Step 5: Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### Step 6: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Visit:  `http://127.0.0.1:8000/`

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=market_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Currency API
CURRENCY_API_KEY=your-currency-api-key
BASE_CURRENCY=UZS

# Click Payment Gateway
CLICK_MERCHANT_ID=your-merchant-id
CLICK_SERVICE_ID=your-service-id
CLICK_SECRET_KEY=your-secret-key

# Payme Payment Gateway
PAYME_MERCHANT_ID=your-merchant-id
PAYME_SECRET_KEY=your-secret-key
PAYME_ENDPOINT=https://checkout.paycom.uz/api

# Google Maps
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Redis
REDIS_URL=redis://localhost:6379/0
```

---

## 💳 Payment Integration

### Click Integration

1. Register merchant account at [click.uz](https://click.uz/)
2. Obtain Merchant ID and Secret Key
3. Configure webhook URL:  `https://yourdomain.com/payments/webhook/click/`
4. Test with test card:  `8600 4954 7331 6478`

### Payme Integration

1. Register at [payme.uz](https://payme.uz/)
2. Configure JSON-RPC endpoint
3. Set webhook URL: `https://yourdomain.com/payments/webhook/payme/`
4. Test with test credentials

### Payment Flow

```
Customer → Checkout → Payment Gateway → Webhook → Order Confirmation
```

---

## 🗄 Database Schema

### Core Tables

- **users** - User accounts and authentication
- **user_profiles** - Extended user information
- **addresses** - User delivery addresses
- **categories** - Product categories (hierarchical)
- **products** - Product catalog
- **product_images** - Multiple images per product
- **product_variants** - Product variations
- **carts** - Shopping carts
- **cart_items** - Cart contents
- **orders** - Customer orders
- **order_items** - Order contents
- **order_status_history** - Order tracking
- **payments** - Payment records
- **transactions** - Payment transaction log
- **reviews** - Product reviews
- **review_images** - Review photos
- **review_votes** - Review helpfulness

### Relationships

```
User (1) ──── (N) Orders
Order (1) ──── (N) OrderItems
Product (1) ──── (N) ProductImages
Product (1) ──── (N) Reviews
Order (1) ──── (N) Payments
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL database
- [ ] Set up Redis for caching
- [ ] Configure HTTPS/SSL
- [ ] Set strong `SECRET_KEY`
- [ ] Configure email backend
- [ ] Set up payment webhooks
- [ ] Configure static/media files
- [ ] Set up monitoring
- [ ] Configure backups

### Docker Deployment

```bash
# Build image
docker build -t market: latest .

# Run container
docker-compose up -d
```

### Traditional Server Deployment

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-dev postgresql nginx

# Configure Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Configure Nginx
# See nginx.conf. example
```

---

## 🔒 Security

### Implemented Security Measures

1. **CSRF Protection** - All forms protected
2. **SQL Injection Prevention** - ORM usage
3. **XSS Prevention** - Template escaping
4. **Password Hashing** - Django's PBKDF2
5. **HTTPS Enforcement** - Production setting
6. **Rate Limiting** - API endpoints
7. **Input Validation** - Form validation
8. **Secure Headers** - Security middleware
9. **Payment Security** - Signature verification
10. **Session Security** - Secure cookies

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.orders

# Coverage report
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## 📊 Performance Optimization

- Database query optimization with `select_related` and `prefetch_related`
- Redis caching for currency rates
- Static file compression with WhiteNoise
- Image optimization with Pillow
- Lazy loading for images
- Database indexing on frequently queried fields

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**TilovovSherzod**

- GitHub: [@TilovovSherzod](https://github.com/TilovovSherzod)
- Email: your-email@example.com

---

## 🙏 Acknowledgments

- Django Community
- Bootstrap Team
- Payment Gateway Providers
- Open Source Contributors

---

## 📞 Support

For support and questions:
- Email: support@market.uz
- Documentation: [docs.market.uz](https://docs.market.uz)
- Issues: [GitHub Issues](https://github.com/TilovovSherzod/market/issues)

---

<div align="center">

**Built with ❤️ for the Central Asian Market**

⭐ Star this repo if you find it helpful! 

</div>"# markett" 
