# AWS EC2 Deployment Guide for Insurance Project

This guide provides step-by-step instructions for deploying the Insurance Django application on an AWS EC2 instance while using Cloudinary for media storage.

## Prerequisites

1. An AWS account
2. A Cloudinary account with your API credentials
3. Basic knowledge of Linux commands
4. A domain name (optional, but recommended for production)

## Step 1: Launch an EC2 Instance

1. Log in to your AWS Management Console
2. Navigate to EC2 Dashboard
3. Click "Launch Instance"
4. Choose an Ubuntu Server AMI (recommended: Ubuntu Server 22.04 LTS)
5. Select an instance type (recommended: t2.micro for testing, t2.small or better for production)
6. Configure instance details as needed
7. Add storage (recommended: at least 20GB)
8. Add tags (optional)
9. Configure security group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
10. Review and launch the instance
11. Create or select an existing key pair and download it
12. Launch the instance

## Step 2: Connect to Your EC2 Instance

1. Open a terminal on your local machine
2. Change permissions for your key file:
   ```
   chmod 400 your-key-file.pem
   ```
3. Connect to your instance:
   ```
   ssh -i your-key-file.pem ubuntu@your-instance-public-dns
   ```

## Step 3: Set Up the Environment

1. Update the system packages:
   ```
   sudo apt update
   sudo apt upgrade -y
   ```

2. Install required packages:
   ```
   sudo apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl build-essential git
   ```

3. Clone your repository:
   ```
   git clone https://your-repository-url.git
   cd your-project-directory
   ```

4. Set up a Python virtual environment:
   ```
   sudo apt install -y python3-venv
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install Python dependencies:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install gunicorn psycopg2-binary
   ```

## Step 4: Set Up PostgreSQL Database

1. Create a database and user:
   ```
   sudo -u postgres psql
   ```

2. In the PostgreSQL prompt, run:
   ```sql
   CREATE DATABASE insurance_db;
   CREATE USER db_user WITH PASSWORD 'your_secure_password';
   ALTER ROLE db_user SET client_encoding TO 'utf8';
   ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE db_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE insurance_db TO db_user;
   \q
   ```

## Step 5: Configure the Application

1. Create a production environment file:
   ```
   cp .env.production .env
   ```

2. Edit the .env file with your specific settings:
   ```
   nano .env
   ```
   
   Update the following:
   - `SECRET_KEY` with a secure random key
   - `ALLOWED_HOSTS` with your domain or EC2 public IP
   - `DATABASE_URL` with your PostgreSQL credentials
   - Ensure your Cloudinary credentials are correct

3. Apply database migrations:
   ```
   python manage.py migrate
   ```

4. Collect static files:
   ```
   python manage.py collectstatic --no-input
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

## Step 6: Configure Gunicorn

1. Copy the Gunicorn configuration file:
   ```
   sudo cp gunicorn_config.py /etc/gunicorn_config.py
   ```

2. Create log and pid directories:
   ```
   sudo mkdir -p /var/log/gunicorn
   sudo mkdir -p /var/run/gunicorn
   sudo chown -R ubuntu:ubuntu /var/log/gunicorn
   sudo chown -R ubuntu:ubuntu /var/run/gunicorn
   ```

## Step 7: Configure Nginx

1. Copy the Nginx configuration file:
   ```
   sudo cp nginx_config /etc/nginx/sites-available/insurance
   ```

2. Edit the configuration file to update paths and domain:
   ```
   sudo nano /etc/nginx/sites-available/insurance
   ```
   
   Update:
   - `server_name` with your domain or EC2 public IP
   - Static files path to match your project's staticfiles directory

3. Create a symbolic link to enable the site:
   ```
   sudo ln -sf /etc/nginx/sites-available/insurance /etc/nginx/sites-enabled/
   ```

4. Test the Nginx configuration:
   ```
   sudo nginx -t
   ```

5. Restart Nginx:
   ```
   sudo systemctl restart nginx
   ```

## Step 8: Set Up Systemd Service

1. Copy the systemd service file:
   ```
   sudo cp systemd_service /etc/systemd/system/insurance.service
   ```

2. Edit the service file to update paths and user:
   ```
   sudo nano /etc/systemd/system/insurance.service
   ```
   
   Update:
   - `User` and `Group` to match your system user
   - `WorkingDirectory` to your project path
   - `ExecStart` path to your Gunicorn executable
   - Environment variables as needed

3. Reload systemd, start and enable the service:
   ```
   sudo systemctl daemon-reload
   sudo systemctl start insurance
   sudo systemctl enable insurance
   ```

4. Check the service status:
   ```
   sudo systemctl status insurance
   ```

## Step 9: Set Up SSL with Let's Encrypt (Optional but Recommended)

1. Install Certbot:
   ```
   sudo apt install -y certbot python3-certbot-nginx
   ```

2. Obtain and install SSL certificates:
   ```
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

3. Follow the prompts to complete the setup
4. Certbot will automatically update your Nginx configuration

## Step 10: Test Your Deployment

1. Open a web browser and navigate to your domain or EC2 public IP
2. Verify that your application is running correctly
3. Test the admin interface at `/admin`
4. Test file uploads to ensure Cloudinary integration is working

## Troubleshooting

### Check Logs

- Gunicorn logs:
  ```
  tail -f /var/log/gunicorn/error.log
  ```

- Nginx logs:
  ```
  tail -f /var/log/nginx/error.log
  ```

- Django logs (if configured):
  ```
  tail -f /path/to/your/django/log/file
  ```

### Common Issues

1. **502 Bad Gateway**
   - Check if Gunicorn is running: `sudo systemctl status insurance`
   - Check Gunicorn error logs
   - Verify the socket configuration in Nginx and Gunicorn

2. **Static Files Not Loading**
   - Check the paths in your Nginx configuration
   - Verify that `collectstatic` ran successfully
   - Check file permissions

3. **Database Connection Issues**
   - Verify PostgreSQL is running: `sudo systemctl status postgresql`
   - Check database credentials in your .env file
   - Ensure the database user has proper permissions

4. **Cloudinary Integration Issues**
   - Verify your Cloudinary credentials
   - Check if the `USE_CLOUDINARY_STORAGE` setting is True
   - Try running `python manage.py migrate_to_cloudinary --no-dry-run`

## Maintenance

### Updating Your Application

1. Pull the latest changes:
   ```
   cd /path/to/your/project
   git pull
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

3. Install any new dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations if needed:
   ```
   python manage.py migrate
   ```

5. Collect static files:
   ```
   python manage.py collectstatic --no-input
   ```

6. Restart the service:
   ```
   sudo systemctl restart insurance
   ```

### Backup

1. Backup your database regularly:
   ```
   sudo -u postgres pg_dump insurance_db > backup_$(date +%Y%m%d).sql
   ```

2. Consider setting up automated backups using AWS Backup or a cron job

### Monitoring

1. Consider setting up monitoring with AWS CloudWatch
2. Monitor your application logs regularly
3. Set up alerts for critical errors

## Security Considerations

1. Keep your system and packages updated
2. Use strong passwords for all services
3. Consider setting up a firewall with UFW
4. Implement rate limiting in Nginx for sensitive endpoints
5. Regularly audit your security settings

## Scaling (Future Considerations)

1. Use an Elastic IP address for your EC2 instance
2. Consider using an Application Load Balancer for high traffic
3. Set up auto-scaling groups for handling traffic spikes
4. Use Amazon RDS for managed database services
5. Implement caching with Redis or Memcached
