#!/usr/bin/env python3
import pika
import sys
import os
from distribution.foundation.logger import Logger

logger = Logger(__name__)

def send_distribution(order):
    try:
      test = channel
    except NameError:
      logger.info("Start publisher for the first time.")
      setup()
      start_queue()
    send_message(order)

def setup():
    global connection, channel, queue_name
    url = os.getenv('CLOUDAMQPURL')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    queue_name = os.getenv('DISTRIBUTIONQ')
    logger.info("setup of publisher completed")

def start_queue():
    channel.queue_declare(queue=queue_name, durable=True)

def send_message(message):
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                             delivery_mode = 2,
                          ))
    logger.info("sent {}".format(message))

def close_connection():
    connection.close()