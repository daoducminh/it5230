# IT4421 - Django Web Application

## Prerequisite

- OS: Linux/MacOS
- Python3
- docker and docker-compose (`Docker version 20.10.1, build 831ebea`
  and `docker-compose version 1.27.4, build 40524192`)

## Deploying

1. Rename file from '.env-example', and rename it to '.env'.: `cp .env-example .env-ci`
2. Run container: `docker-compose up`.
3. Open browser with url: `http://localhost` or `http://127.0.0.1`
4. Sample accounts:

   |Type|Username|Password|
   |---|---|---|
   |admin|admin_01|1a2s3d4f|
   |user|user_01|1a2s3d4f|