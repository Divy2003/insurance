# AWS EC2 Deployment Guide for Insurance Project

This guide outlines the steps taken to deploy the Insurance Django application on AWS EC2 with Nginx, Gunicorn, and PostgreSQL.

## Prerequisites

- AWS EC2 instance running Ubuntu
- Domain name (optional)
- PostgreSQL database
- Cloudinary account for media storage

## Deployment Steps

### 1. Set Up EC2 Instance

- Launch an EC2 instance with Ubuntu
- Configure security groups to allow HTTP (port 80), HTTPS (port 443), and SSH (port 22)
- Connect to your instance via SSH

### 2. Install Required Packages

```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx git
```

### 3. Clone the Repository

```bash
git clone https://github.com/Divy2003/insurance.git
cd insurance/Agent
```

### 4. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 5. Configure PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE insurance_db;
CREATE USER db_user WITH PASSWORD '1234divy';
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE insurance_db TO db_user;
\q
```

### 6. Configure Gunicorn

Create directories for Gunicorn logs and socket:

```bash
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R ubuntu:ubuntu /var/log/gunicorn
sudo chown -R ubuntu:ubuntu /var/run/gunicorn
```

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/insurance.service
```

Add the following content:

```
[Unit]
Description=Insurance Django Application
After=network.target postgresql.service

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/insurance/Agent
ExecStart=/home/ubuntu/insurance/Agent/venv/bin/gunicorn insurance.wsgi:application --bind=127.0.0.1:8000
Restart=on-failure
Environment="PATH=/home/ubuntu/insurance/Agent/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=insurance.settings"
Environment="DEBUG=False"
Environment="AWS_DEPLOYMENT=True"
Environment="CLOUD_NAME=dc1dzbv7o"
Environment="API_KEY=your_api_key"
Environment="API_SECRET=your_api_secret"
Environment="CLOUDINARY_URL=cloudinary://your_api_key:your_api_secret@dc1dzbv7o"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable insurance
sudo systemctl start insurance
sudo systemctl status insurance
```

### 7. Configure Nginx

Create an Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/insurance
```

Add the following content:

```
server {
    listen 80;
    server_name 51.20.248.221;  # Replace with your domain name or server IP

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    # Serve static files directly
    location /static/ {
        alias /home/ubuntu/insurance/Agent/staticfiles/;  # Path to your static files
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # Proxy requests to Gunicorn
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
        proxy_buffering off;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Increase max upload size for large files
    client_max_body_size 10M;
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_proxied any;
    gzip_vary on;
    gzip_types
        application/atom+xml
        application/javascript
        application/json
        application/ld+json
        application/manifest+json
        application/rss+xml
        application/vnd.geo+json
        application/vnd.ms-fontobject
        application/x-font-ttf
        application/x-web-app-manifest+json
        application/xhtml+xml
        application/xml
        font/opentype
        image/bmp
        image/svg+xml
        image/x-icon
        text/cache-manifest
        text/css
        text/plain
        text/vcard
        text/vnd.rim.location.xloc
        text/vtt
        text/x-component
        text/x-cross-domain-policy;
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/insurance /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site if it exists
sudo nginx -t  # Test Nginx configuration
sudo systemctl restart nginx
```

### 8. Collect Static Files and Set Permissions

```bash
python manage.py collectstatic --noinput
sudo chown -R www-data:www-data /home/ubuntu/insurance/Agent/staticfiles/
sudo chmod -R 755 /home/ubuntu/insurance/Agent/staticfiles/
sudo chmod +x /home
sudo chmod +x /home/ubuntu
sudo chmod +x /home/ubuntu/insurance
sudo chmod +x /home/ubuntu/insurance/Agent
```

### 9. Fix for Agent Profile Update

If you encounter a 500 error when updating the agent profile, you need to modify the `admin_views.py` file to handle the case where there is no agent:

```python
@custom_admin_required
def admin_agent(request):
    agent = Agent.objects.first()  # Assuming only one agent
    
    if agent is None:
        # Create a new agent if none exists
        agent = Agent(
            name="Your Name",
            email="your.email@example.com",
            phone="123-456-7890",
            bio="Professional insurance agent with over 15 years of experience."
        )
        agent.save()

    if request.method == 'POST':
        agent.name = request.POST.get('name')
        agent.email = request.POST.get('email')
        agent.phone = request.POST.get('phone')
        agent.bio = request.POST.get('bio')

        if 'profile_picture' in request.FILES:
            agent.profile_picture = request.FILES['profile_picture']

        agent.save()
        messages.success(request, 'Agent profile updated successfully')
        return redirect('custom_admin_agent')

    return render(request, 'admin/agent_edit.html', {'agent': agent})
```

After making this change, restart the Gunicorn service:

```bash
sudo systemctl restart insurance
```

## Accessing Your Website

Your website should now be accessible at your EC2 instance's public IP address:

```
http://51.20.248.221
```

## Troubleshooting

### Static Files Not Loading

If static files are not loading, check the permissions:

```bash
sudo chown -R www-data:www-data /home/ubuntu/insurance/Agent/staticfiles/
sudo chmod -R 755 /home/ubuntu/insurance/Agent/staticfiles/
sudo chmod +x /home
sudo chmod +x /home/ubuntu
sudo chmod +x /home/ubuntu/insurance
sudo chmod +x /home/ubuntu/insurance/Agent
sudo systemctl restart nginx
```

### 500 Server Error

Check the logs for more details:

```bash
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u insurance
```

## Maintenance

### Restarting Services

```bash
sudo systemctl restart insurance
sudo systemctl restart nginx
```

### Updating the Application

```bash
cd /home/ubuntu/insurance
git pull
cd Agent
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
sudo systemctl restart insurance
```
