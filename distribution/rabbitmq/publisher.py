#!/usr/bin/env python3
import pika
import sys
import os
from distribution.foundation.logger import Logger
import pika.exceptions as pikex

logger = Logger(__name__)

def send_distribution(order):
    try:
      test = channel
    except NameError:
      logger.info("Start publisher for the first time.")
      setup()
      start_queue()
    try:
      send_message(order)
    except pikex.ConnectionClosed:
      logger.warning("Connection closed, retrying...")
      setup()
      start_queue()
      send_distribution(order)

def setup():
    global connection, channel, queue_name
    url = os.getenv('RABBITMQ_URL')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    queue_name = os.getenv('DISTRIBUTION_QUEUE')
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