#!/usr/bin/env python3
import pika
import os
import sys
from distribution.foundation.logger import Logger
from distribution.foundation.exceptions import DomainException
from requests.exceptions import RequestException
from service import demand_service

logger = Logger(__name__)

def main():
    setup()
    start_worker()

def setup():
    global channel, queue_name
    url = os.getenv('CLOUDAMQPURL')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    queue_name = os.getenv('ROUTEQ')
    logger.info("setup of worker completed")

def start_worker():
    start_queue()
    start_channel()

def start_queue():
    channel.exchange_declare(exchange='newx', exchange_type='fanout')
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
        demand_service.update_demand(body)
    except DomainException as domainex:
        logger.critical(domainex)
    except RequestException as requex:
        logger.critical(requex)
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    main()