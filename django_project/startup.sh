#!/bin/bash

echo "\n>>>>> Migrating the database before starting the server\n"
python manage.py makemigrations
python manage.py migrate

echo "\n>>>>> Unzip data\n"
unzip -o data.zip

echo "\n>>>>> Load data\n"
python manage.py loaddata data.json

echo "\n>>>>> Update score\n"
python manage.py update_score

echo "\n>>>>> Run server\n"
python manage.py runserver 0.0.0.0:8000
