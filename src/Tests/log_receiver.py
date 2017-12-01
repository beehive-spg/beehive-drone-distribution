#!/usr/bin/env python
import pika
import os


class TLR:

	def __init__(self):
		self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://stwbdmln:mMBizAx37OVGGHHTkslHVRVhN1SVOOx5@lark.rmq.cloudamqp.com/stwbdmln')
		self.params = pika.URLParameters(self.url)
		self.connection = pika.BlockingConnection(self.params)
		self.channel = self.connection.channel()

	def start_queue(self):
		self.result = self.channel.queue_declare(exclusive=True)
		self.queue_name = self.result.method.queue
		print(' [*] Waiting for logs. To exit press CTRL+C')

	def start_listening(self, ch, method, properties, body):
	    print(" [x] %r" % body)

	def start_channel(self):
		self.channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
		self.channel.queue_bind(exchange='logs',
                   queue=self.queue_name)
		self.channel.basic_consume(self.start_listening,
                      queue=self.queue_name,
                      no_ack=True)
		self.channel.start_consuming()
