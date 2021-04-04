FROM python:3.8.9-slim-buster

WORKDIR /app
ENV FLASK_APP=webapp_stores
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#FROM celery:latest as celery
#EXPOSE 5000:5000
CMD ["flask", "run"]





