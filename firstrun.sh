#!/usr/bin/env bash

echo "creating virtualenv..."
virtualenv -p /usr/local/bin/python3 ../apienv > /dev/null
echo "virtualenv created and activated"
source ../apienv/bin/activate
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
echo "populating database..."
./manage.py runscript populate_db
echo "running server..."
./manage.py runserver_plus
