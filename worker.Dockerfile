FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y redis-server

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD service redis-server start && celery -A cloud_conversion_tool.celery_script beat -l info & celery -A cloud_conversion_tool.celery_script worker -l info
