FROM python:3.7-slim
RUN mkdir /code
WORKDIR /code
ENV FLASK_APP webapp_stores
ENV FLASK_RUN_HOST 0.0.0.0
ADD webapp_stores /code/
COPY requirements.txt /code
RUN pip install -r requirements.txt
#RUN celery flower -A tasks --address=0.0.0.0 --port=5555
#RUN celery -A tasks beat
#RUN celery -A tasks worker
EXPOSE 5000
COPY . .
CMD ["flask", "run"]



