#!/bin/bash

echo "Ждём запуск БД"
sleep 5
echo "Накатываем миграции в БД"
echo "******"
alembic upgrade head
echo "******"

echo "Добавляем стандартных юзеров"
python add_default_roles.py

echo "Выполнено"

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
