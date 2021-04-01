FROM python:3.7-slim

WORKDIR /code
ENV FLASK_APP webapp_stores
ENV FLASK_RUN_HOST 0.0.0.0
ADD webapp_stores .
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000:5000


CMD ["flask", "run"]





