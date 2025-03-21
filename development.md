# Описание



## Модерирование проекта

Модерирование проектом осуществляется с помощью файла с переменными окружениями.

Перед запуском проекта необходимо создать копию `.env.example` и переименовать ее в `.env`
Далее необходимо изменить необходимые переменные:

```
#############################################
# FastAPI environment variables
#############################################
PROJECT_NAME=fastapi-sqlmodel-alembic
FIRST_SUPERUSER_PASSWORD=admin
FIRST_SUPERUSER_EMAIL=admin@admin.com
ENCRYPT_KEY=TshgGacKPYrm35m89UqbRg46JAbUm2yRtxOCQFdqa3w=
SECRET_KEY=09d25e0sas4faa6c52gf6c818166b7a9563b93f7sdsdef6f0f4caa6cf63b88e8d3e7
BACKEND_CORS_ORIGINS=["*"] 

#############################################
# PostgreSQL database environment variables
#############################################
POSTGRESQL_HOST=database
POSTGRESQL_USERNAME=postgres
POSTGRESQL_PASSWORD=postgres
POSTGRESQL_DATABASE=fastapi_db
DATABASE_CELERY_NAME=celery_schedule_jobs
POSTGRESQL_PORT=5432

#############################################
# Caddy variables (Переменные окружения для Реверс-прокси)
#############################################
EXT_ENDPOINT1=127.0.0.1
LOCAL_1=localhost
LOCAL_2=127.0.0.1
CADDY_PORT=80

#############################################
# Redis variables
#############################################
REDIS_HOST=redis_server
REDIS_PORT=6379

#############################################
# Minio variables
#############################################
MINIO_URL=storage.localhost
MINIO_BUCKET=fastapi-minio
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

#############################################
# Wheater
#############################################
WHEATER_URL=https://wttr.in

#############################################
# OpenAPI variables
#############################################
OPENAI_API_KEY=
```

# Запуск сервера Fast Api

[Инструкция по запуску сервера](\backend\development.md)

# Подключение к Redis 

Подключение к Redis осуществляется с помощью расширения `cweijan.vscode-redis-client` в VSCode

## Из devcontainer

Host: redis_server
Port: 6379
Username: <Пусто>
Password: <Пусто>


# Подключение к PostgreSQL

Подключение к PotgreSQL осуществляется с помощью расширения `cweijan.dbclient-jdbc` в VSCode

## Из devcontainer
Host: database
Port: 5432
Database: fastapi_db
Username: postgres
Password: postgres
