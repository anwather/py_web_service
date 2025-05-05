#!/bin/bash
# 
# Deployment Script for Test Web Connectivity Service
# This script installs and configures the web service on an Ubuntu server
#

set -e  # Exit on error

echo "==============================================="
echo "  Test Web Connectivity Service Deployment Script"
echo "==============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo"
  exit 1
fi

# Install dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-pip python3-venv

# Create a directory for the service
SERVICE_DIR="/opt/py_web_service"
echo "Creating service directory at $SERVICE_DIR..."
mkdir -p $SERVICE_DIR

# Copy files to the service directory
echo "Where are the web service files located? (Enter path or press Enter for current directory)"
read SOURCE_DIR
SOURCE_DIR=${SOURCE_DIR:-$(pwd)}

echo "Copying files from $SOURCE_DIR to $SERVICE_DIR..."
cp -r $SOURCE_DIR/* $SERVICE_DIR/

# Create a virtual environment and install dependencies
echo "Setting up Python virtual environment..."
cd $SERVICE_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create a systemd service
echo "Creating systemd service..."
cat > /etc/systemd/system/py-web-service.service << EOF
[Unit]
Description=Test Web Connectivity Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$SERVICE_DIR
ExecStart=$SERVICE_DIR/venv/bin/python3 $SERVICE_DIR/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure file permissions
echo "Setting file permissions..."
chown -R www-data:www-data $SERVICE_DIR
chmod +x $SERVICE_DIR/app.py

# Enable and start the service
echo "Enabling and starting the service..."
systemctl daemon-reload
systemctl enable py-web-service
systemctl start py-web-service

# Configure firewall if ufw is active
if command -v ufw &> /dev/null && ufw status | grep -q "active"; then
    echo "Configuring firewall..."
    # Read the port from config file
    PORT=$(grep -A1 "server:" $SERVICE_DIR/config.yaml | grep "port:" | awk '{print $2}')
    PORT=${PORT:-5000}  # Default to 5000 if not found
    ufw allow $PORT/tcp
    echo "Allowed access to port $PORT"
fi

echo "==============================================="
echo "  Deployment Complete!"
echo "==============================================="
echo "The web service is now running."
echo "You can access it at: http://$(hostname -I | awk '{print $1}'):$(grep -A1 "server:" $SERVICE_DIR/config.yaml | grep "port:" | awk '{print $2}')"
echo "To check the service status: systemctl status py-web-service"
echo "==============================================="