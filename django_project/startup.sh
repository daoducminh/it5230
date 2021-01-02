#!/bin/bash

echo ">>>>> Migrating the database before starting the server"
python manage.py makemigrations
python manage.py migrate

echo ">>>>> Load data"
python manage.py loaddata data.json

echo ">>>>> Update score"
python manage.py update_score

echo ">>>>> Run server"
python manage.py runserver 0.0.0.0:8000
