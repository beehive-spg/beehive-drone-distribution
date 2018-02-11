#!/usr/bin/env python3
import pika
import sys
import os
import json

class TTP:

	def __init__(self, message):
		url = os.environ.get('CLOUDAMQP_URL', os.environ['CLOUDAMQPURL'])
		params = pika.URLParameters(url)
		self.message = message
		self.queue_name = "workload_prediction_queue"
		self.connection = pika.BlockingConnection(params)
		self.channel = self.connection.channel()

	def start_queue(self):
		self.channel.queue_declare(queue=self.queue_name, durable=True)
		
	def send_message(self):
		self.channel.basic_publish(exchange='',
                  routing_key=self.queue_name,
                  body=self.message,
                  properties=pika.BasicProperties(
                     delivery_mode = 2, # make message persistent
                  ))
		print(" [x] Sent %r" % self.message)

	def close_connection(self):
		self.connection.close()
			

