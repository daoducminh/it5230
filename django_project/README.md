# IT4421 - Django Web Application

## Prerequisite

- OS: Linux/MacOS
- Python3
- docker and docker-compose (`Docker version 20.10.1, build 831ebea`
  and `docker-compose version 1.27.4, build 40524192`)

## Deploying

1. Create `.evn-ci` file with these settings:
   ```
   SECRET_KEY=n6jzfo%$k91@jf1-w4ci9!5yhhso2(hqq5x+@1r6d&-=sv6!+0
   
   DB_ENGINE=django.db.backends.postgresql_psycopg2
   DB_HOST=db
   DB_PORT=5432
   DB_DATABASE=django
   DB_USERNAME=hello
   DB_PASSWORD=world123
   ```
2. Run container: `docker-compose up`.
3. Open browser with url: `http://localhost` or `http://127.0.0.1`
4. Sample accounts:

   |Type|Username|Password|
   |---|---|---|
   |admin|minhdao|1a2s3d4f|
   |user|test|y5GSL3LmAbHr8rF|