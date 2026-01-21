#!/bin/bash

# Markett - Elastic Beanstalk Deploy Script
# Usage: ./eb-deploy.sh [environment]

set -e

echo "🚀 Markett Elastic Beanstalk Deploy Script"
echo "=========================================="

# Set environment (default: production)
ENV_NAME=${1:-markett-production}

echo "📦 Environment: $ENV_NAME"
echo ""

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "❌ Error: EB CLI is not installed"
    echo "Install it with: pip install awsebcli"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "✅ Please edit .env file with your settings before deploying"
    exit 1
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Check for migrations
echo "🔍 Checking for pending migrations..."
if python manage.py showmigrations | grep -q '\[ \]'; then
    echo "⚠️  Warning: You have pending migrations"
    read -p "Do you want to continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create deployment package
echo "📦 Creating deployment package..."
git add -A
git commit -m "Deploy to Elastic Beanstalk - $(date)" || echo "No changes to commit"

# Deploy to Elastic Beanstalk
echo "🚀 Deploying to $ENV_NAME..."
eb deploy $ENV_NAME

echo ""
echo "✅ Deployment completed!"
echo ""
echo "🌐 To open your application:"
echo "   eb open $ENV_NAME"
echo ""
echo "📊 To check logs:"
echo "   eb logs $ENV_NAME"
echo ""
echo "💻 To SSH into instance:"
echo "   eb ssh $ENV_NAME"
