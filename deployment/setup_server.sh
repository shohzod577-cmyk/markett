#!/bin/bash

# AWS EC2 Server Setup Script for Markett Django Application
# Run this script on a fresh Ubuntu 22.04 EC2 instance

set -e

echo "============================================"
echo "Markett Django Application - Server Setup"
echo "============================================"

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "Installing Python 3.11 and dependencies..."
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
sudo apt install -y build-essential libpq-dev nginx git curl

# Install PostgreSQL client
echo "Installing PostgreSQL client..."
sudo apt install -y postgresql-client

# Install Redis
echo "Installing Redis..."
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /home/ubuntu/markett
sudo chown ubuntu:ubuntu /home/ubuntu/markett

# Create logs directory
echo "Creating logs directory..."
mkdir -p /home/ubuntu/markett/logs

# NOTE: Project files should already be copied to /home/ubuntu/markett
echo "INFO: Make sure project files are in /home/ubuntu/markett"
echo "If not copied yet, use: scp -i key.pem -r Markett ubuntu@ip:/home/ubuntu/markett"

# Create Python virtual environment
echo "Creating Python virtual environment..."
cd /home/ubuntu/markett
python3.11 -m venv venv
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp deployment/.env.example .env
    echo "Created .env file from .env.example"
    echo "IMPORTANT: Edit /home/ubuntu/markett/.env with your actual credentials!"
fi

# Setup PostgreSQL database (if using local PostgreSQL instead of RDS)
# Uncomment if needed:
# echo "Setting up PostgreSQL..."
# sudo apt install -y postgresql postgresql-contrib
# sudo systemctl enable postgresql
# sudo systemctl start postgresql
# sudo -u postgres psql -c "CREATE DATABASE markett_db;"
# sudo -u postgres psql -c "CREATE USER markett_user WITH PASSWORD 'your-password';"
# sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE markett_db TO markett_user;"

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (interactive)
echo "Creating Django superuser..."
echo "You can skip this and create it later with: python manage.py createsuperuser"
# python manage.py createsuperuser

# Setup Gunicorn systemd service
echo "Setting up Gunicorn service..."
sudo cp deployment/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# Setup Celery systemd service
echo "Setting up Celery service..."
sudo cp deployment/celery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable celery
sudo systemctl start celery

# Setup Nginx
echo "Setting up Nginx..."
sudo cp deployment/nginx.conf /etc/nginx/sites-available/markett
sudo ln -sf /etc/nginx/sites-available/markett /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

# Setup firewall
echo "Configuring firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "============================================"
echo "Server setup completed!"
echo "============================================"
echo ""
echo "IMPORTANT NEXT STEPS:"
echo "1. Edit /home/ubuntu/markett/.env with your actual credentials"
echo "2. Update deployment/nginx.conf with your domain name"
echo "3. Run: sudo systemctl restart gunicorn"
echo "4. Run: sudo systemctl restart nginx"
echo "5. Create superuser: python manage.py createsuperuser"
echo "6. Setup SSL with Let's Encrypt: sudo certbot --nginx -d your-domain.com"
echo ""
echo "Check service status:"
echo "  sudo systemctl status gunicorn"
echo "  sudo systemctl status celery"
echo "  sudo systemctl status nginx"
echo ""
echo "View logs:"
echo "  tail -f /home/ubuntu/markett/logs/gunicorn-error.log"
echo "  tail -f /home/ubuntu/markett/logs/celery.log"
echo "  sudo tail -f /var/log/nginx/error.log"
