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

## Запуск

Запуск сервера осуществляется из консоли внутри devcontainer. Команда:
```
gunicorn -w 3 -k uvicorn.workers.UvicornWorker travel_ai_backend.app.main:app  --bind 0.0.0.0:8000 --preload --log-level=debug --timeout 120
```