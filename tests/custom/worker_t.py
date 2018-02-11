#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from rabbitmq import worker
import publisher_for_worker_test

def main():
	setup()
	test_worker_message_receiving()

def setup():
	global python_version, worker_directory
	python_version = 'python3'
	worker_directory = '../rabbitmq/'

def test_worker_message_receiving():
	publisher_for_worker_test.main()
	worker.main()

if __name__ == '__main__':
	main()