FROM python:3.7-slim

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user
COPY ./tasks.py /home/user
COPY ./celeryconfig.py /home/user
RUN pip install redis

RUN pip install celery=="4.4.6"

RUN { \
	echo 'import os'; \
	echo "BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://')"; \
} > celeryconfig.py

USER user
#CMD ["celery", "worker"]