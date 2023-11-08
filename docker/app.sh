#!/bin/bash

echo "my location is"
echo pwd
echo "Накатываем миграции в БД"
alembic upgrade head
echo "Накатили миграции, запускаем гуникорм"
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
echo "Сервер запущен !"