#!/usr/bin/env python
import pika
import sys
import os


class TTP:

	def __init__(self):
		self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://stwbdmln:mMBizAx37OVGGHHTkslHVRVhN1SVOOx5@lark.rmq.cloudamqp.com/stwbdmln')
		self.params = pika.URLParameters(self.url)
		self.connection = pika.BlockingConnection(self.params)
		self.channel = self.connection.channel()

	def start_queue(self):
		self.channel.queue_declare(queue='task_queue', durable=True)
		
	def send_message(self):
		self.message = ' '.join(sys.argv[1:]) or "Hello World!"
		self.channel.basic_publish(exchange='',
                  routing_key='task_queue',
                  body=self.message,
                  properties=pika.BasicProperties(
                     delivery_mode = 2, # make message persistent
                  ))
		print(" [x] Sent %r" % self.message)

	def send_log(self):
		self.channel.exchange_declare(exchange='logs',
		                         exchange_type='fanout')

		self.log_message = ' '.join(sys.argv[1:]) or "info: Hello World!"
		self.channel.basic_publish(exchange='logs',
		                      routing_key='',
		                      body=self.log_message)
		print(" [x] Sent %r" % self.log_message)
		self.connection.close()

