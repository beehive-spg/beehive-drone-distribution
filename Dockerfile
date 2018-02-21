FROM python:3

COPY /distribution .
COPY requirements.txt .
COPY .env .

RUN pip3 install -r ../requirements.txt

EXPOSE 5671:5671

ENTRYPOINT [ "python3", "./rabbitmq/worker.py" ]