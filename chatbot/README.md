# Setup Chatbot Project

## Create network
    docker network create internal-network

## Install Mysql-client (for test)
    Ubuntu:
        sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

    MacOs:
        brew install mysql-client pkg-config
        export PKG_CONFIG_PATH="$(brew --prefix)/opt/mysql-client/lib/pkgconfig"

    export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs mysqlclient)
    export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags mysqlclient)
    pip install mysqlclient

## Setup Requirements
    pip install -r requirements.txt

## Init Project
    django-admin startproject fsdl .

## Init App
    django-admin startapp memo


## Update fsdl/settings.py
    INSTALLED_APPS = [
        'memo',
        ...
    ]
    

## Migration
    python manage.py makemigrations
    python manage.py migrate

## Create user
    docker exec -it chatbot-web bash
    python manage.py createsuperuser

## Run server
    python manage.py runserver 0.0.0.0:8001

## Deploy
    docker compose up -d --build

## Create collection (index)
    http://localhost:6333/dashboard#/collections

    curl --location 'http://localhost:8000/chat/collection/create' \
        --header 'Content-Type: application/json' \
        --data '{
            "collection_name": "llm"
        }'

## References
- https://docs.djangoproject.com/en/5.1/intro/tutorial01/

