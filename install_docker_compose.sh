#!/bin/bash

# Check if Docker Compose is already installed
if command -v docker-compose &>/dev/null; then
    echo "Docker Compose is already installed."
    exit 0
fi

# Install Docker Compose
echo "Installing Docker Compose..."

# Install required dependencies
sudo apt-get update
sudo apt-get install -y curl jq

# Get the latest release version of Docker Compose
latest_release=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r '.tag_name')

# Download Docker Compose binary
sudo curl -L "https://github.com/docker/compose/releases/download/${latest_release}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to the Docker Compose binary
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version

echo "Docker Compose installation completed."

# # EXECUTION
# # Open a terminal, find install_docker_compose.sh, and then make it executable:

# $ chmod +x install_docker_compose.sh
# # You can then run the script with sudo permissions:

# $ sudo ./install_docker_compose.sh