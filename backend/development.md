# Запуск сервера Fast Api

Сервер доступен по адресу: `https://fastapi.localhost`

Документация доступна по адресу: `https://fastapi.localhost/docs`

## Миграции

Для создании базы данных, если она еще не создана нужно применить миграции:
```
alembic upgrade head
```

Если миграций нет, необходимо их создать:
```
alembic revision --autogenerate
```

Далее для инициализации базы данных их необходимо применить:
```
alembic upgrade head
```

## Создание самоподписных сертификатов

Установите OpenSSL: Если у вас еще не установлен OpenSSL, вы можете установить его с помощью команды `apt-get install openssl`

Создайте приватный ключ с помощью команды:
`openssl genrsa -out certs/server.key 2048`

Создайте сертификатный запрос: Создайте сертификатный запрос с помощью команды:
`openssl req -new -key ./certs/server.key -out ./certs/server.csr`

Создайте самоподписанный сертификат: Создайте самоподписанный сертификат с помощью команды:
`openssl x509 -req -days 365 -in ./certs/server.csr -signkey ./certs/server.key -out ./certs/server.crt`


## Запуск

Запуск сервера осуществляется из консоли внутри devcontainer. Команда:
```
gunicorn -w 3 -k uvicorn.workers.UvicornWorker travel_ai_backend.app.main:app  --bind 0.0.0.0:8000 --certfile ./certs/server.crt --keyfile ./certs/server.key --preload --log-level=debug --timeout 120
```