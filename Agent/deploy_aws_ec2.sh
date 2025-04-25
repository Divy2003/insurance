#!/bin/bash
# AWS EC2 Deployment Script for Insurance Project

# Exit on error
set -e

echo "Starting deployment process..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl build-essential

# Install Python virtual environment
echo "Setting up Python virtual environment..."
sudo apt-get install -y python3-venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Set up PostgreSQL database
echo "Setting up PostgreSQL database..."
# Note: You should manually create the database and user with proper credentials
# sudo -u postgres psql -c "CREATE DATABASE insurance;"
# sudo -u postgres psql -c "CREATE USER insuranceuser WITH PASSWORD 'your_password';"
# sudo -u postgres psql -c "ALTER ROLE insuranceuser SET client_encoding TO 'utf8';"
# sudo -u postgres psql -c "ALTER ROLE insuranceuser SET default_transaction_isolation TO 'read committed';"
# sudo -u postgres psql -c "ALTER ROLE insuranceuser SET timezone TO 'UTC';"
# sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE insurance TO insuranceuser;"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Check if we should use Cloudinary for storage
if [ -n "$CLOUDINARY_URL" ] || ([ -n "$CLOUDINARY_CLOUD_NAME" ] && [ -n "$CLOUDINARY_API_KEY" ] && [ -n "$CLOUDINARY_API_SECRET" ]); then
    echo "Cloudinary configuration detected. Using Cloudinary for media storage..."
    # Migrate existing media to Cloudinary if needed
    python manage.py migrate_to_cloudinary --no-dry-run
else
    echo "No Cloudinary configuration found. Using local storage."
    # Copy media files to static directory for production
    python manage.py copy_media_to_static
fi

# Set up Gunicorn
echo "Setting up Gunicorn..."
sudo cp gunicorn_config.py /etc/gunicorn_config.py

# Set up Nginx
echo "Setting up Nginx..."
sudo cp nginx_config /etc/nginx/sites-available/insurance
sudo ln -sf /etc/nginx/sites-available/insurance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up systemd service
echo "Setting up systemd service..."
sudo cp systemd_service /etc/systemd/system/insurance.service
sudo systemctl daemon-reload
sudo systemctl start insurance
sudo systemctl enable insurance

echo "Deployment completed successfully!"
echo "Your application should now be running at http://your_server_ip"
