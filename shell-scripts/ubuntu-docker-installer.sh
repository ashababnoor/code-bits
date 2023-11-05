#!/bin/bash

password=$1

sudo apt update
sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install -y docker-ce
sudo usermod -aG docker ${USER}
echo $password | su - ${USER}
sudo apt install -y docker-compose

echo -e "\n"
echo "Successfully installed Docker and Docker-Compose"
echo "Run the following command to check docker service status"
echo -e "\n"
echo -e "\t sudo systemctl status docker"
echo -e "\n"