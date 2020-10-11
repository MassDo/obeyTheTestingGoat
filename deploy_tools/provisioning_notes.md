Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* pip
* Git

eg, on Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python3.6 python3-pip

## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., staging.my-domain.com

## Folder structure:

Assume we have a user account at /home/username

```
/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
```

## Provisioning with Fabric:

Server side:

```bash
sudo apt-get update && sudo apt-get install nginx
```

Local:
```python
fab deploy:host=<USER_NAME>@<YOUR_DOMAIN>
```

## Deployment: 

Create nginx conf file on server side

```bash
cat ./deploy_tools/nginx.template.conf \
| sed "s/DOMAIN/<YOUR_DOMAIN>/g" \
| sed "s/USER_NAME/<YOUR_USER_NAME>/g" \
| sudo tee /etc/nginx/sites-available/<YOUR_DOMAIN>
```

Activate with symbolic link

```bash
sudo ln -s /etc/nginx/sites-available/<YOUR_DOMAIN> \
/etc/nginx/sites-enabled/<YOUR_DOMAIN>
```

Write Systemd service

```bash
cat ./deploy_tools/gunicorn.systemd.template.service \
| sed "s/DOMAIN/<YOUR_DOMAIN>/g" \
| sed "s/USER_NAME/<YOUR_USER_NAME>/g" \
| sed "s/PROJECT_NAME/<PROJECT_NAME>/g" \
| sudo tee /etc/systemd/system/gunicorn-<YOUR_DOMAIN>.service
```

Start both services

```bash
sudo systemctl daemon-reload && \
sudo systemctl reload nginx && \
sudo systemctl enable gunicorn-<YOUR_DOMAIN>.service && \
sudo systemctl start gunicorn-<YOUR_DOMAIN>.service
```

