#!/bin/bash

# Deployment Script for Markett Django Application
# Run this script to update the application on AWS EC2

set -e

echo "============================================"
echo "Deploying Markett Django Application"
echo "============================================"

# Navigate to project directory
cd /home/ubuntu/markett

# Activate virtual environment
source venv/bin/activate

# Update code (if using git, otherwise skip)
if [ -d .git ]; then
    echo "Pulling latest code from repository..."
    git pull origin main
else
    echo "Skipping git pull (not a git repository)"
    echo "To update: copy new files via SCP"
fi

# Install/update dependencies
echo "Installing/updating Python packages..."
pip install -r requirements.txt --upgrade

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Compile translation files
echo "Compiling translation files..."
python manage.py compilemessages

# Restart Gunicorn
echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

# Restart Celery
echo "Restarting Celery..."
sudo systemctl restart celery

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "============================================"
echo "Deployment completed successfully!"
echo "============================================"

# Check service status
echo ""
echo "Service Status:"
sudo systemctl status gunicorn --no-pager -l
sudo systemctl status celery --no-pager -l
sudo systemctl status nginx --no-pager -l

echo ""
echo "Recent logs:"
echo "--- Gunicorn Logs ---"
tail -20 /home/ubuntu/markett/logs/gunicorn-error.log

echo ""
echo "--- Celery Logs ---"
tail -20 /home/ubuntu/markett/logs/celery.log
