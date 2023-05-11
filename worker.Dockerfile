FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y redis-server

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 ./cloud_conversion_tool/worker_pubsub/tasks.py
