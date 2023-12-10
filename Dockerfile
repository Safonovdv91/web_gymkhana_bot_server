# Этап 1: Установка зависимостей с помощью poetry
FROM python:3.10-slim AS builder

# Устанавливаем переменную окружения для корректной работы Python в контейнере
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости для poetry
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -sSL https://install.python-poetry.org | python3 -

# Добавляем путь к установленным бинарным файлам poetry в переменную PATH
ENV PATH="${PATH}:/root/.local/bin"

# Копируем файлы проекта в контейнер
COPY pyproject.toml poetry.lock /app/

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости проекта с помощью poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Этап 2: Установка зависимостей для запуска приложения
FROM python:3.10-slim AS dependencies

# Устанавливаем переменную окружения для корректной работы Python в контейнере
ENV PYTHONUNBUFFERED=1

# Копируем зависимости из первого этапа
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости для запуска приложения
RUN pip install uvicorn gunicorn alembic

# Этап 3: Запуск приложения
FROM python:3.10-slim
LABEL authors="safon"


# Устанавливаем переменную окружения для корректной работы Python в контейнере
ENV PYTHONUNBUFFERED=1

# Копируем зависимости из второго этапа
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app
RUN chmod a+x app.sh

# Открываем порт, на котором будет запущен FastAPI
#EXPOSE 9000

# Запускаем FastAPI при старте контейнера
#CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
#--------------
#FROM python:3.10
#LABEL authors="safon"

#RUN mkdir /fastapi_app
#WORKDIR /fastapi_app

#COPY requirements.txt .

#RUN pip install -r requirements.txt
#COPY . .

#RUN chmod a+x app.sh
#CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000