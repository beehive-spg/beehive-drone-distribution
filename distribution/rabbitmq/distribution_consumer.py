#!/usr/bin/env python3
import pika
import os
import sys
import time
from distribution.service import demandservice
from distribution.foundation.logger import Logger
from distribution.foundation.exceptions import DomainException
from requests.exceptions import RequestException
from pika.exceptions import ConnectionClosed

logger = Logger(__name__)

def main(distribution_status, queue):
    global dist_status, q
    dist_status = distribution_status
    q = queue
    while(True):
        try:
            setup()
            break
        except ConnectionClosed:
            logger.info("RabbitMQ - waiiiiting for connection...")
            time.sleep(5)
    start_consumer()

def setup():
    global channel, queue_name
    url = os.getenv('RABBITMQ_URL')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    queue_name = os.getenv('DISTRIBUTION_EVENT_QUEUE')
    logger.info("RabbitMQ - Connection successful")

def start_consumer():
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
    global dist_status
    try:
        if (not q.empty()):
            incoming_status = q.get()
            if(incoming_status != dist_status):
                dist_status = incoming_status
                logger.info("------------changed distribution status: {}".format(dist_status))
            else:
                q.put(incoming_status)
        demandservice.update_demand(body, dist_status)
    except DomainException as domainex:
        logger.critical(domainex)
    except RequestException as requex:
        logger.critical(requex)
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    main()