# Stack Schools

[![Python Version](https://img.shields.io/badge/python-3.12-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-6.0.5-brightgreen.svg)](https://djangoproject.com)
[![CircleCI](https://circleci.com/gh/suhailvs/django-schools.svg?style=svg)](https://circleci.com/gh/suhailvs/django-schools)

urls:
+ asm /schools/32060200110/
+ kerala /schools/21009/
+ limeric_college /bp/351803/
+ /postalcodes/678686/

## Deployment

Install Apache:
```bash
apt-get update
apt-get install python3-pip nginx postgresql postgresql-contrib libpq-dev
sudo -u postgres psql

ALTER USER postgres WITH PASSWORD 'root';
create database stackschools;
```
Create virtual and install django:

```bash
cd /var/www/
git clone https://github.com/suhailvs/stackschools
cd stackschools
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
mkdir media
chown www-data:www-data media
cp .env.sample .env # update it
./manage.py collectstatic
./manage.py migrate
```

#### Add gunicorn and nginx config :

```ini
$ vim /etc/systemd/system/stackschools.socket
[Unit]
Description=Stackschools socket

[Socket]
ListenStream=/run/stackschools.sock

[Install]
WantedBy=sockets.target
```

```ini
$ vim /etc/systemd/system/stackschools.service
[Unit]
Description=Stackschools Gunicorn daemon for Django
Requires=stackschools.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/stackschools
ExecStart=/var/www/stackschools/env/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/stackschools.sock \
    mysite.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
systemctl enable stackschools
systemctl start stackschools
systemctl status stackschools
```

nginx settings:
```
$ vim /etc/nginx/sites-available/stackschools
server {
    listen 80;
    server_name stackschools.com www.stackschools.com;
    location = /robots.txt {
        alias /var/www/stackschools/robots.txt;
    }
    location = /ads.txt {
        alias /var/www/stackschools/ads.txt;
    }
	location = /favicon.ico { 
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
	location /static/ {
        alias /var/www/stackschools/staticfiles/;
    }
	location /media/ {
        alias /var/www/stackschools/media/;
	}
    location / {
        proxy_pass http://unix:/run/stackschools.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
	error_log /var/www/stackschools/media/error.log;
}
```

Enable it:
```bash
sudo ln -s /etc/nginx/sites-available/stackschools /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**lets encrypt for HTTPS**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d stackschools.com -d www.stackschools.com
```

