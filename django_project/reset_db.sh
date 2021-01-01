#!/usr/bin/env bash

# Remove all tables
python manage.py reset_db

# Remove migration files
mv foods/migrations/__init__.py foods/migrations/__init__
rm foods/migrations/*.py
mv foods/migrations/__init__ foods/migrations/__init__.py

# Migration
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.json
