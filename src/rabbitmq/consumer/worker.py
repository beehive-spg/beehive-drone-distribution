#!/usr/bin/env python
import pika
import os

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

def start_worker():
	start_queue()
	start_channel()

def start_queue():
	channel.queue_declare(queue=queue_name, durable=True)

def start_channel():
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(on_response,
                      queue=queue_name)
	channel.start_consuming()

def on_response(ch, method, properties, body):
	print(" [x] Received %r" % body)
	ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    main()