#!/bin/bash
# =============================================================================
# AWS Cloud Internship Project: EC2 Automated Setup Script
# =============================================================================
# Run this script on an Ubuntu 22.04 or 24.04 LTS EC2 instance:
#   sudo bash infra/setup_ec2.sh
# =============================================================================

set -e

echo "=== [1/6] Updating System & Installing Prerequisites ==="
apt-get update -y
apt-get install -y python3-pip python3-venv git nginx curl ufw

echo "=== [2/6] Preparing Application Directory ==="
APP_DIR="/var/www/AWS-internship"
if [ ! -d "$APP_DIR" ]; then
    mkdir -p /var/www
    cd /var/www
    git clone https://github.com/madhumitha19022-spec/AWS-internship.git
fi

cd "$APP_DIR"
git pull origin main || true

echo "=== [3/6] Setting Up Python Virtual Environment ==="
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Create .env if not present
if [ ! -f ".env" ]; then
    cat <<EOT > .env
AWS_REGION=ap-south-1
S3_BUCKET_NAME=aws-internship-portal-madhumitha
FLASK_DEBUG=False
PORT=5000
HOST=127.0.0.1
EOT
fi

echo "=== [4/6] Creating Systemd Service for Gunicorn ==="
cat <<EOT > /etc/systemd/system/internship-portal.service
[Unit]
Description=Gunicorn daemon serving AWS Internship Portal
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/AWS-internship
EnvironmentFile=/var/www/AWS-internship/.env
ExecStart=/var/www/AWS-internship/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl enable internship-portal
systemctl restart internship-portal

echo "=== [5/6] Configuring Nginx Reverse Proxy (Port 80 -> 5000) ==="
cat <<EOT > /etc/nginx/sites-available/internship-portal
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
EOT

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/internship-portal /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

echo "=== [6/6] Verifying Local Deployment Health ==="
sleep 2
HEALTH_STATUS=$(curl -s http://127.0.0.1/health || echo "FAILED")
echo "Health Check Result: $HEALTH_STATUS"

echo "============================================================================="
echo " SUCCESS! The AWS Internship Portal is live and running on Port 80."
echo " Access the website at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || hostname -I | awk '{print $1}')"
echo "============================================================================="
