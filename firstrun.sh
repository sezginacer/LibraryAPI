#!/usr/bin/env bash

if ! command -v python3 > /dev/null 2>&1; then
    echo "python3 not found, please install and try again!"
elif ! command -v pip > /dev/null 2>&1; then
    echo "pip not found, please install and try again!"
elif ! command -v virtualenv > /dev/null 2>&1; then
    echo "virtualenv not found, please install and try again!"
else
    echo "creating virtualenv..."
    virtualenv -p $(which python3) venv > /dev/null
    echo "virtualenv created and activated"
    source venv/bin/activate
    pip install --upgrade virtualenv > /dev/null
    echo "installing requirements..."
    pip install -r requirements.txt > /dev/null
    echo "requirements installed"
    echo "creating database schema..."
    ./manage.py migrate > /dev/null
    echo "db schema created"
    echo "creating user..."
    ./manage.py runscript create_user --traceback
    echo "username > admin"
    echo "password > admin"
    echo "user created"
    echo "populating database..."
    ./manage.py runscript populate_db
    echo "running server..."
    ./manage.py runserver_plus
fi
