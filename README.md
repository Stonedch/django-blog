# Django Blog

Django Blog is an open source blog built with *Django*. 

## Table of contents

* [Setup](#setup)
* [Status](#status)
* [Contacts](#contacts)

## Setup

1. Create the environments file:

    ```console
    foo@bar: django-blog $ cp .env.sample .env
    ```

2. Build docker images and up containers:

    ```console
    foo@bar: django-blog $ docker-compose up -d --build
    ```

3. Make migrations and migrate:

    ```console
    foo@bar: django-blog $ docker-compose exec webserver python manage.py makemigrations

    foo@bar: django-blog $ docker-compose exec webserver python manage.py migrate
    ```

4. Create super user:

    ```console
    foo@bar: django-blog $ docker-compose exec webserver python manage.py createsuperuser
    ```

## Status

Project is: _in progress_

## Contacts

Created by [@stonedch](https://github.com/stonedch)
