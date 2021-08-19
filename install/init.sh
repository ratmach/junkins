#!/bin/bash

read -p "Please specify the port (i.e 8083):" -e -i 8083 port
read -p "Please specify the user (i.e user):" -e -i 'user' user
read -p "Please specify the user_group (i.e www-data):" -e -i 'www-data' user_group
read -p "Please specify the domain/IP (nginx server, i.e 0.0.0.0):" -e -i '0.0.0.0' ip

read -p "Please specify junkins folder" -e -i '/junkins' junkins_root

read -p "Install python? [y/n] y" -e python_install

if [[ "$python_install" == "n" || "$python_install" == "N" ]]; then
  echo ">>> Skipping python installation"
else
  echo ">>> Installing python"
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt update
  sudo apt install python3.8
fi

echo "Installing nginx"
read -p "Install nginx? [y/n] y" -e nginx_install

if [[ "$nginx_install" == "n" || "$nginx_install" == "N" ]]; then
  echo ">>> Skipping nginx installation"
else
  echo ">>> Installing nginx"
  sudo apt-get install nginx
  python3 scripts/get-pip.py
fi

echo "Setting up venv"
python3 -m pip install virtualenv
cd "$junkins_root"

mkdir junkins_venv
virtualenv junkins_venv
source junkins_venv/bin/activate

echo "Installing Dependencies"
python3 -m pip install -r requirements.txt

echo "Building configuration files"
cd install
python3 make_gunicorn_file.py "$user" "$user_group" "$junkins_junkins_root"
python3 make_nginx_file.py "$port" "$ip" "$junkins_root"

echo "Copying configuration files"
sudo cp gunicorn.service /etc/systemd/gunicorn.service
sudo cp nginx.service /etc/nginx/sites-available/junkins

echo "Registering gunicorn service"
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo "Updating nginx configuration"
sudo ln -s /etc/nginx/sites-available/junkins /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow $port

mkdir scripts
