## Jenkins' younger cousin.

Primitive CI/CD pipeline which assigns custom bash script to an endpoint
with primitive security measures (not recommended for production environments)

## Installation
clone repository:

```git clone https://github.com/ratmach/junkins```

install script:

``chmod +x install.sh``

``./install.sh``

OR:
1. Install and configure nginx:
   1. ``sudo apt-get install nginx``
2. install virtualenv ``pip install virtualenv``
3. create virtual env: 
   1. ``mkdir ~/junkins``
   2. ``cd ~/junkins``
   3. ``virtualenv junkins_venv``
   4. ``source junkins_venv/bin/activate``
4. install dependencies ``pip install -r requirements.txt``
5. create gunicorn service:
   1. ``sudo nano /etc/systemd/gunicorn.service``
   2. ```text
      [Unit]
      Description=gunicorn daemon
      After=network.target
         
      [Service]
      User=user
      Group=www-data
      WorkingDirectory=/home/user/jenkins
      ExecStart=/home/user/jenkins/jenkins_venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/junkins/junkins.sock junkins.wsgi:app
         
      [Install]
      WantedBy=multi-user.target
   3. add gunicorn service to systemctl:
      1. ```sudo systemctl start gunicorn```
      2. ```sudo systemctl enable gunicorn```
      3. ```sudo systemctl status gunicorn```
6. configure nginx to pass proxy requests to gunicorn:
   1. ```text
      server {
          listen 8083;
          server_name your_domain www.your_domain;
      
          location / {
            include proxy_params;
            proxy_pass http://unix:/home/sammy/myproject/myproject.sock;
          }
      }
   2. ``sudo ln -s /etc/nginx/sites-available/junkins /etc/nginx/sites-enabled``
   3. ``sudo nginx -t``
   4. ``sudo systemctl restart nginx``
   5. add exception to firewall ``sudo ufw allow 8083``
7. add scripts to "script\"
8. add configuration to config.json

## CONFIGURATION:

configuration is done in config.json
with format:

```json
{
  "port": 8083,
  "scripts": [
    {
      "endpoint": "/pull/",
      "auth_type": "BASIC_HTTP",
      "token": "",
      "credentials": {
        "username": "rage",
        "password": "123"
      },
      "script": "pull.sh"
    }
  ]
}
```

environment variable "CONF LOCATION" can also be set in order to allow for several instances of the server