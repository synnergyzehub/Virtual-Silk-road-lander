#!/bin/bash

echo "Starting Genesis Backend Deployment..."
sudo apt update && sudo apt upgrade -y

echo "Installing Python, pip, Docker, and Compose..."
sudo apt install -y python3 python3-pip docker.io docker-compose

echo "Creating project directory..."
mkdir -p ~/genesis_stack && cd ~/genesis_stack

echo "Downloading Genesis Backend Toolkit..."
curl -O http://localhost:8000/genesis_backend_toolkit.zip
unzip genesis_backend_toolkit.zip

echo "Installing Python requirements..."
pip3 install flask flask-cors

echo "Launching Docker services..."
docker-compose -f genesis_mysql_docker_compose.yml up -d

echo "Starting Genesis API server..."
nohup python3 genesis_api.py > genesis_api.log 2>&1 &

echo "Genesis backend is now live."
