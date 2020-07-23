FROM python:3.7-slim
RUN mkdir /app
WORKDIR /app
ENV FLASK_APP /webapp_stores
ENV FLASK_RUN_HOST 0.0.0.0
ADD . /app
COPY . .
COPY requirements.txt .
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
RUN pip install -r requirements.txt
EXPOSE 5000

#CMD ["flask", "run"]



