FROM python:3-alpine

RUN mkdir beehive-drone-distribution

COPY /distribution beehive-drone-distribution/distribution
COPY requirements.txt beehive-drone-distribution
COPY .env beehive-drone-distribution

RUN pip3 install -r beehive-drone-distribution/requirements.txt

WORKDIR /beehive-drone-distribution/distribution

ENTRYPOINT [ "python3", "op.py" ]