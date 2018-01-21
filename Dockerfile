FROM python:3

COPY /drone_distribution .
COPY requirements.txt .
COPY .env .

RUN pip3 install -r ../requirements.txt

EXPOSE 5671:5671

CMD [ "python", "./op.py" ]
