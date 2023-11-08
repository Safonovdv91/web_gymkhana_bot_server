#!/bin/bash

echo "my location is"
echo "Накатываем миграции в БД"
alembic -c alembic.ini upgrade head
echo "******"
echo "******"
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
