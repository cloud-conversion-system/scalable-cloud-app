FROM python:3.9-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

CMD cd cloud_conversion_tool && python3 -m flask run --host=0.0.0.0 -p 80
