#!/usr/bin/env python
import pika
import time
import os

class Worker:

	def __init__(self):
		self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://stwbdmln:mMBizAx37OVGGHHTkslHVRVhN1SVOOx5@lark.rmq.cloudamqp.com/stwbdmln')
		self.params = pika.URLParameters(self.url)
		self.connection = pika.BlockingConnection(self.params)
		self.channel = self.connection.channel()

	def start_queue(self):
		self.channel.queue_declare(queue='workload_prediction_queue', durable=True)
		print(' [*] Waiting for messages. To exit press CTRL+C')

	def on_response(self, ch, method, properties, body):
	    print(" [x] Received %r" % body)
	    time.sleep(body.count(b'.'))
	    print(" [x] Done")
	    ch.basic_ack(delivery_tag = method.delivery_tag)

	def start_channel(self):
		self.channel.basic_qos(prefetch_count=1)
		self.channel.basic_consume(self.on_response,
	                      queue='task_queue')
		self.channel.start_consuming()
