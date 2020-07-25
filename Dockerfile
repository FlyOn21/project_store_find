#FROM python:3.7-slim
#
#RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
#WORKDIR /home/user
#COPY ./tasks.py /home/user
#COPY ./celeryconfig.py /home/user
#RUN pip install redis
#
#RUN pip install celery=="4.4.6"
#
#RUN { \
#	echo 'import os'; \
#	echo "BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://')"; \
#} > celeryconfig.py
#
#USER user
#CMD ["celery", "worker"]
FROM python:3.7-slim as app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
COPY . /app

FROM nginx:1.18-alpine as nginx
#EXPOSE 5000
COPY ./static/ /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d