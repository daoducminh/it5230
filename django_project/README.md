# IT4421 - Django Web Application

## Prerequisite

- OS: Linux/MacOS
- Python3
- docker and docker-compose (`Docker version 20.10.1, build 831ebea`
  and `docker-compose version 1.27.4, build 40524192`)

## Installation

1. Install global packages: `python3 -m pip install virtualenv`
2. Create virtualenv for project: `virtualenv .venv`
3. Activate virtualenv: `source .venv/bin/activate`
4. Install required packages: `python -m pip install -r requirements.txt`
5. Rename file from '.env-example', and rename it to '.env'.: `cp .env-example .env`
6. Configure PostgreSQL:
    - Switch to `postgres` user: `sudo -i -u postgres`
    - Create PSQL user: `createuser --interactive --pwprompt` (skip if you already have it). Then fill answers for
      prompts, for example:
      |Prompt|Answer| |---|---| |Enter name of role to add:|hello| |Enter password for new role:|world123| |Enter it
      again:|world123| |Shall the new role be a superuser?|y|
    - Create database for user (skip if you already have it): `createdb hello`
    - Create database for Django: `createdb django`
7. Migrate databases: `python manage.py makemigrations && python manage.py migrate`
8. Run server: `python manage.py runserver`

## Seeding data

1. Generate fake data: `.venv/bin/python seeds.py`
2. Load data: `.venv/bin/python manage.py loaddata foods.json`

## Deploying

1. Checkout branch `deploy`: `git checkout deploy`
2. Rename file from '.env-example', and rename it to '.env'.: `cp .env-example .env-ci`
3. Run container: `docker-compose up`.
4. Open browser with url: `http://localhost` or `http://127.0.0.1`
5. Sample accounts:

   |Type|Username|Password|
   |---|---|---|
   |admin|minhdao|1a2s3d4f|
   |user|test|y5GSL3LmAbHr8rF|