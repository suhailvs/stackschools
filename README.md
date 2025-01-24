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

	$ python3 -m venv env
	$ source ./env/bin/activate
	$ apt install libpq-dev
	$ apt install gdal-bin
	$ apt install postgis
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

		AliasMatch ^/sitemap-(.*) /var/www/stackschools/sitemaps/sitemap-$1
		Alias /sitemap.xml /var/www/stackschools/sitemaps/sitemap.xml
		Alias /robots.txt /var/www/stackschools/staticfiles/robots.txt
		Alias /ads.txt /var/www/stackschools/ads.txt
		Alias /favicon.ico /var/www/stackschools/staticfiles/favicon.ico
		Alias /media/ /var/www/stackschools/media/
		Alias /static/ /var/www/stackschools/staticfiles/
		
		<Directory /var/www/stackschools/staticfiles>
		Require all granted
		</Directory>
		<Directory /var/www/stackschools/media>
		Require all granted
		</Directory>
		
		WSGIDaemonProcess stackschoolapp python-home=/var/www/stackschools/env python-path=/var/www/stackschools/
		WSGIProcessGroup stackschoolapp
		WSGIScriptAlias / /var/www/stackschools/mysite/wsgi.py
		# ErrorLog /var/www/stackschools/media/error.log
		# CustomLog /var/www/stackschools/media/access.log combined
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
```


**migrate:**

    ./manage.py migrate


**Load School Database**

	git clone https://github.com/sta-k/stackschools_datas
	cd stackschools_datas
	tar xvf data_sql.tar.xz
	psql -U postgres -d stackschools < keralaschools.sql
	psql -U postgres -d stackschools < schools.sql
	psql -U postgres -d stackschools < colleges.sql
	rm keralaschools.sql schools.sql colleges.sql

**Dump database**

	sudo su postgres
	pg_dump --data-only -d stackschools -t <table_name> > /tmp/file.sql

#### Create and upload sitemaps

**update django core sitemap**

since urls in `sitemap.xml` will look like `sitemap-college.xml?p=3` so need to change it to `sitemap-college3.xml`, to fix edit django file `env/lib/python3.12/site-packages/django/contrib/sitemaps/views.py` line 85 with::

	SitemapIndexItem(absolute_url.replace('.xml',f'{page}.xml'), site_lastmod)

**update mysite/urls.py**

uncomment sitempas in `mysite/urls.py`::

	path('sitemap.xml', sitemaps_views.index, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemaps_views.sitemap, {'sitemaps': my_sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
     
**generate sitemap**

	./manage.py generate_sitemap

zip `sitemaps` folder inside `media`, then copy it to `github.com/sta-k/stackschools_datas`. then commit and push

**upload sitemaps to server**

pull the changes in stackschools_datas and move folder `sitemaps` to `/var/www/stackschools/`.

