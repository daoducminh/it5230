# IT4421

## Prerequisite
- Ubuntu 18.04 or above

## Installation
1. Install required packages:
```bash
sudo ./install.sh
```
2. Configure PostgreSQL:
    > Sample configuration
    > ```
    > DB_CONNECTION=pgsql
    > DB_HOST=127.0.0.1
    > DB_PORT=5432
    > DB_DATABASE=laravel
    > DB_USERNAME=hello
    > DB_PASSWORD=world123
    > ```

    - Switch to `postgres` user: `sudo -i -u postgres`
    - Create PSQL user: `createuser --interactive --pwprompt`. Then fill answers for prompts, for example:
        |Prompt|Answer|
        |---|---|
        |Enter name of role to add:|hello|
        |Enter password for new role:|world123|
        |Enter it again:|world123|
        |Shall the new role be a superuser?|y|
    - Create database for user: `createdb hello`
    - Create database for Laravel: `createdb laravel`
3. Configure Laravel project:
    - Create `.env` file with configuration. For example:
        ```
        APP_NAME=Laravel
        APP_ENV=local
        APP_KEY=base64:tRbl/Job1/D3qq/lhtow35CydDNUt11LswMeKcP3Oq0=
        APP_DEBUG=true
        APP_URL=http://localhost

        LOG_CHANNEL=stack
        LOG_LEVEL=debug

        DB_CONNECTION=pgsql
        DB_HOST=127.0.0.1
        DB_PORT=5432
        DB_DATABASE=laravel
        DB_USERNAME=hello
        DB_PASSWORD=world123

        BROADCAST_DRIVER=log
        CACHE_DRIVER=file
        QUEUE_CONNECTION=sync
        SESSION_DRIVER=database
        SESSION_LIFETIME=120

        REDIS_HOST=127.0.0.1
        REDIS_PASSWORD=null
        REDIS_PORT=6379

        MAIL_MAILER=smtp
        MAIL_HOST=smtp.mailtrap.io
        MAIL_PORT=2525
        MAIL_USERNAME=null
        MAIL_PASSWORD=null
        MAIL_ENCRYPTION=null
        MAIL_FROM_ADDRESS=null
        MAIL_FROM_NAME="${APP_NAME}"

        AWS_ACCESS_KEY_ID=
        AWS_SECRET_ACCESS_KEY=
        AWS_DEFAULT_REGION=us-east-1
        AWS_BUCKET=

        PUSHER_APP_ID=
        PUSHER_APP_KEY=
        PUSHER_APP_SECRET=
        PUSHER_APP_CLUSTER=mt1

        MIX_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
        MIX_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
        ```
        Your local address will be `localhost:8000`
    - Migrate schemas: in project folder, run: `php artisan migrate`
    - Start development server: `php artisan serve`