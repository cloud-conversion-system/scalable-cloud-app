FROM python:3.9-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR "/python-docker/cloud_conversion_tool"

EXPOSE 80

CMD [ "celery", "-A", "vistas/vistas", "worker", "-l", "info"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "-p", "80"]