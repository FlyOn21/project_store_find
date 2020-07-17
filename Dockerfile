FROM python:3.7
RUN mkdir /code
WORKDIR /code
ADD webapp_stores /code/
COPY requirements.txt /code
RUN pip install -r requirements.txt
RUN celery -A webapp_stores/tasks.py worker -B




