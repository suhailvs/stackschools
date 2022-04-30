FROM python:3.7.4-alpine3.10

ADD requirements.txt /app/requirements.txt
ADD db.sqlite3 /app/db.sqlite3

RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt
    
ADD . /app
ADD mysite/static/ /app/staticfiles
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "mysite.wsgi"]