# Stack Schools

[![Python Version](https://img.shields.io/badge/python-3.8-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.1-brightgreen.svg)](https://djangoproject.com)
[![CircleCI](https://circleci.com/gh/suhailvs/django-schools.svg?style=svg)](https://circleci.com/gh/suhailvs/django-schools)

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/suhailvs/stackschools
```

Create Virtual Env and Install the requirements:

```bash
cd stackschools
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Deployment

Install Apache:

	$ apt-get update
	$ apt-get install python3-pip apache2 libapache2-mod-wsgi-py3

+ Change dir: `$ cd /var/www/`
+ Clone the repo: `$ git clone https://github.com/suhailvs/stackschools`
+ Change dir: `$ cd stackschools`

Create virtual and install django:

	$ pip3 install virtualenv
	$ virtualenv env
	$ source ./env/bin/activate
	$ apt install libpq-dev
	$ pip install -r requirements.txt
	$ mkdir media
	$ chown www-data:www-data media
	$ cp .env.sample .env # update it
	$ ./manage.py collectstatic


Edit apache config :


Django conf:

	$ vim /etc/apache2/sites-available/stackschools.conf

	<VirtualHost *:80>
		ServerName stackschools.com
		ServerAlias www.stackschools.com

		Alias /robots.txt /var/www/stackschools/staticfiles/robots.txt
		Alias /favicon.ico /var/www/stackschools/staticfiles/favicon.ico
		Alias /media/ /var/www/stackschools/media/
		Alias /static/ /var/www/stackschools/staticfiles/
		Alias /docsstudent /var/www/stackschools/docs/student/_build/html/

		<Directory /var/www/stackschools/docs>
        Require all granted
        </Directory>
		<Directory /var/www/stackschools/staticfiles>
		Require all granted
		</Directory>
		<Directory /var/www/stackschools/media>
		Require all granted
		</Directory>
		
		WSGIDaemonProcess stackschoolapp python-home=/var/www/stackschools/env python-path=/var/www/stackschools/
		WSGIProcessGroup stackschoolapp
		WSGIScriptAlias / /var/www/stackschools/mysite/wsgi.py
		ErrorLog /var/www/stackschools/media/error.log
		CustomLog /var/www/stackschools/media/access.log combined
	</VirtualHost>


**lets encrypt for HTTPS**


I had to comment the `WSGIDaemonProcess` line out before running letsencrypt.

	$ vim /etc/apache2/sites-available/stackschools.conf
	<VirtualHost *:80>
		...
		# WSGIDaemonProcess stackschoolapp python-home=/var/www/stackschools/env python-path=/var/www/stackschools/

install certbot and run it.

	apt-get install python3-certbot-apache
	a2ensite stackschools.conf
	service apache2 restart
	certbot --apache -d stackschools.com -d www.stackschools.com

Then uncommented `WSGIDaemonProcess` in `stackshools.conf` and `stackschools-le-ssl.conf` and in `stackschools-le-ssl.conf` change `stackschoolapp` to `stackschoolappssl`.


restart apache: 

	$ a2ensite stackschools.conf
	$ service apache2 reload

## Create the database:

#### You might need to install postgresql:

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql

ALTER USER postgres WITH PASSWORD 'root';
create database stackschools;
update pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'stackschools';
```


**migrate:**

    ./manage.py migrate


**Load School Database**

	tar xvf data.tar.xz
	psql -U postgres -d stackschools < keralaschools.sql
	psql -U postgres -d stackschools < schools.sql
	rm keralaschools.sql schools.sql

**Dump database**

	pg_dump --data-only -d stackschools -t <table_name> > /tmp/file.sql

## Todo

* need to remove `core` app