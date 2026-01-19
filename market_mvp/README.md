MARKET MVP (market_mvp)

Overview
- Minimal, production-minded Django scaffold with a custom `users` app.

Quickstart
1. Create and activate virtualenv
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
2. Install deps
   pip install -r requirements.txt
3. Run migrations
   python manage.py migrate
4. Start server
   python manage.py runserver

Notes
- Settings support Postgres via environment variables (`DB_ENGINE` etc.).
- This scaffold is intentionally minimal; next steps: implement products, cart, orders, payments, dashboard.
