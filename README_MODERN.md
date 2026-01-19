# 🛍️ Markett - Modern E-Commerce Platform

Uzum Market-style modern online marketplace built with Django 4.2

![Markett Banner](https://via.placeholder.com/1200x300/7000ff/ffffff?text=Markett+-+Modern+E-Commerce)

## ✨ Features

### 🎨 Modern UI/UX
- **Uzum Market-inspired Design** - Purple gradient theme with modern components
- **Fully Responsive** - Works perfectly on all devices (mobile, tablet, desktop)
- **Smooth Animations** - CSS transitions and hover effects
- **Dark Navbar** - Sticky navigation with gradient logo
- **Product Cards** - Modern cards with badges, favorites, and quick actions
- **Image Gallery** - Interactive product image viewer with thumbnails

### 🛒 E-Commerce Features
- **Product Management** - Categories, filters, search, and sorting
- **Shopping Cart** - Modern cart with quantity controls and totals
- **Wishlist** - Save favorite products
- **User Authentication** - Login, register, profile management
- **Order Management** - Complete checkout and order tracking
- **Payment Integration** - Multiple payment gateways support
- **Reviews & Ratings** - Customer feedback system

### 🌍 Internationalization
- **Multi-language Support** - Uzbek, Russian, English
- **Multi-currency** - UZS, USD, RUB
- **RTL Support Ready** - Can be enabled for Arabic/Persian

### 🔒 Security & Performance
- **Django 4.2** - Latest stable version
- **CSRF Protection** - Secure form submissions
- **XSS Prevention** - Sanitized user inputs
- **Lazy Loading** - Images load on demand
- **Caching** - Redis integration ready
- **Optimized Queries** - Using select_related and prefetch_related

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+ (or SQLite for development)
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/markett.git
cd markett
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Database setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Load initial data (optional)**
```bash
python manage.py loaddata categories products
```

7. **Compile translations**
```bash
python manage.py compilemessages
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## 📁 Project Structure

```
Markett/
├── apps/
│   ├── cart/           # Shopping cart functionality
│   ├── dashboard/      # Admin dashboard
│   ├── orders/         # Order management
│   ├── payments/       # Payment processing
│   ├── products/       # Product catalog
│   ├── reviews/        # Product reviews
│   └── users/          # User authentication
├── config/             # Django settings
├── static/
│   ├── css/
│   │   ├── modern-style.css    # Main modern styles
│   │   └── style.css           # Legacy styles
│   ├── js/
│   │   └── markett-modern.js   # JavaScript functionality
│   └── images/
├── templates/
│   ├── base.html              # Base layout
│   ├── home.html              # Homepage
│   ├── 404.html, 403.html, etc.  # Error pages
│   ├── cart/
│   │   └── cart_modern.html   # Shopping cart
│   ├── products/
│   │   ├── product_card.html        # Reusable product card
│   │   ├── product_detail_modern.html  # Product details
│   │   └── product_list_modern.html    # Products listing
│   └── partials/
│       ├── navbar.html        # Navigation header
│       └── footer.html        # Footer with newsletter
└── manage.py
```

## 🎨 Design System

### Color Palette
- **Primary**: `#7000ff` (Purple)
- **Secondary**: `#ff1f7f` (Pink)
- **Accent**: `#00d4aa` (Teal)
- **Background**: `#f8f9fa` (Light Gray)
- **Text**: `#1a1a1a` (Dark Gray)

### Typography
- **Font Family**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Headings**: 700 weight, larger sizes
- **Body**: 400 weight, 1rem base size

### Components
- **Buttons**: Rounded (12px), gradient backgrounds, hover effects
- **Cards**: Soft shadows, 16px border-radius, hover lift
- **Badges**: Small labels with colored backgrounds
- **Forms**: Modern inputs with purple focus states

## 🛠️ Technologies Used

### Backend
- **Django 4.2.9** - Web framework
- **PostgreSQL** - Database
- **Celery** - Task queue
- **Redis** - Caching & sessions
- **Pillow** - Image processing

### Frontend
- **Bootstrap 5.3.2** - UI framework
- **Bootstrap Icons 1.11.1** - Icon library
- **Vanilla JavaScript** - No jQuery dependency
- **CSS3** - Modern animations and gradients

### DevOps
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy
- **Docker** - Containerization
- **GitHub Actions** - CI/CD

## 📱 Pages

1. **Home** (`/`) - Hero section, featured products, categories
2. **Products** (`/products/`) - Grid view with filters and sorting
3. **Product Detail** (`/products/<slug>/`) - Image gallery, specifications, reviews
4. **Cart** (`/cart/`) - Shopping cart with order summary
5. **Checkout** (`/checkout/`) - Multi-step checkout process
6. **Profile** (`/profile/`) - User dashboard with orders
7. **Orders** (`/orders/`) - Order history and tracking

## 🔧 Configuration

### Environment Variables
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost/markett
REDIS_URL=redis://localhost:6379/1
```

### Settings
- `config/settings.py` - Main Django settings
- `config/urls.py` - URL routing
- Language codes: `uz`, `ru`, `en`
- Currency codes: `UZS`, `USD`, `RUB`

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

With coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

## 📦 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Use PostgreSQL database
- [ ] Configure Redis for caching
- [ ] Set up Celery workers
- [ ] Configure email backend
- [ ] Enable HTTPS
- [ ] Set up static/media file serving
- [ ] Configure backups

### Docker Deployment
```bash
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shohzod**
- GitHub: [@shohzod](https://github.com/shohzod)
- Email: shohzod@example.com

## 🙏 Acknowledgments

- Design inspired by [Uzum Market](https://uzum.uz)
- Icons by [Bootstrap Icons](https://icons.getbootstrap.com/)
- Color palette from [Coolors](https://coolors.co/)

## 📞 Support

For support, email shohzod@example.com or join our Telegram group.

---

Made with ❤️ in Uzbekistan
