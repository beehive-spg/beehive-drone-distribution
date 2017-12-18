#!/usr/bin/env python3
import pika
import sys
import os
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')

def send_distribution(order):
	setup()
	start_queue()
	send_message(order)
	close_connection()

def setup():
	global connection, channel, queue_name
	url = os.environ.get('CLOUDAMQP_URL', os.environ['CLOUDAMQPURL'])
	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	queue_name = 'drone_distribution'
	logging.info("setup of publisher completed")

def start_queue():
	channel.queue_declare(queue=queue_name, durable=True)
		
def send_message(message):
	channel.basic_publish(exchange='',
              routing_key=queue_name,
              body=message,
              properties=pika.BasicProperties(
                 delivery_mode = 2,
              ))
	logging.info("sent {}".format(message))

def close_connection():
	connection.close()