FROM python:3-alpine

WORKDIR app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY distribution distribution

ARG settings_queue
ARG distribution_event
ARG distribution_queue
ARG rabbitmq
ARG database

ENV SETTINGS_QUEUE=$settings_queue
ENV DISTRIBUTION_EVENT_QUEUE=$distribution_event
ENV DISTRIBUTION_QUEUE=$distribution_queue
ENV RABBITMQ_URL=$rabbitmq
ENV DATABASE_URL=$database

CMD python3 distribution/op.py