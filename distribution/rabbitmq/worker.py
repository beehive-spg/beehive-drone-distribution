#!/usr/bin/env python3
import pika
import os
import sys
import logging
from distribution import operator

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')

def main():
	setup()
	start_worker()

def setup():
	global channel, queue_name
	url = os.environ.get('CLOUDAMQP_URL', os.environ['CLOUDAMQPURL'])
	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	queue_name = 'workload_prediction_queue'
	logging.info("setup of worker completed")

def start_worker():
	start_queue()
	start_channel()

def start_queue():
	channel.queue_declare(queue=queue_name, durable=True)
	logging.info("started {}".format(queue_name))

def start_channel():
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(on_response,
                      queue=queue_name)
	logging.info("listening to queue")
	channel.start_consuming()

def on_response(ch, method, properties, body):
	operator.handle_message(body)
	logging.info("received {}".format(body))
	ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    main()