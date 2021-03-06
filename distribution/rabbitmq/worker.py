#!/usr/bin/env python3
import pika
import os
import sys
from distribution.service import demandservice
from distribution.foundation.logger import Logger
from distribution.foundation.exceptions import DomainException
from requests.exceptions import RequestException

logger = Logger(__name__)

def main():
    setup()
    start_worker()

def setup():
    global channel, queue_name
    url = os.getenv('RABBITMQ_URL')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    queue_name = os.getenv('DISTRIBUTION_EVENT_QUEUE')
    logger.info("RabbitMQ - Connection successful")

def start_worker():
    start_queue()
    start_channel()

def start_queue():
    channel.exchange_declare(exchange='eventx', exchange_type='fanout')
    channel.queue_declare(queue=queue_name, durable=True)
    logger.info("started {}".format(queue_name))

def start_channel():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_response,
                      queue=queue_name)
    logger.info("listening to queue")
    channel.start_consuming()

def on_response(ch, method, properties, body):
    try:
        demandservice.update_demand(body)
    except DomainException as domainex:
        logger.critical(domainex)
    except RequestException as requex:
        logger.critical(requex)
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    main()