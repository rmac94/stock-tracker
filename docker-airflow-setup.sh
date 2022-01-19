#!/bin/bash

#Install docker
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
#Y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce

#Install Docker-Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Download airflow and configure folders / env variables
mkdir airflow-docker && cd airflow-docker
curl -LfO 'http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/docker-compose.yaml'
mkdir ./dags ./plugins ./logs
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

#Change docker-compose to match python version on instance
sed -i 's/airflow:2.3.0.dev0/airflow:2.2.3-python3.6/g' docker-compose.yaml

#initialise airflow instance
sudo docker-compose up airflow-init
#sudo docker-compose up