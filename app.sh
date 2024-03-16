#!/bin/bash

echo "Ждём запуск БД"
sleep 2
echo "Накатываем миграции в БД"
echo "******"
alembic upgrade head
echo "******"

echo "Запустили py-scripts"
python add_default_roles.py

echo "Выполнено"

gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
