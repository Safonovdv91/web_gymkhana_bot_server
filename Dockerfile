FROM python:3.10
LABEL authors="safon"

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

RUN chmod a+x docker/*.sh
#CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000