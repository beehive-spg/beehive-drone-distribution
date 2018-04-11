#!/usr/bin/env python3
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from multiprocessing import Process, Queue
from distribution.rabbitmq import distribution_consumer
from distribution.rabbitmq import settings_consumer
from pika.exceptions import ConnectionClosed
from distribution.foundation.logger import Logger

logger = Logger(__name__)

def main():
    distribution_status = 0 #off
    queue = Queue()
    p1 = Process(target=settings_consumer.main, args=(distribution_status, queue))
    p2 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p3 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p1.start()
    p2.start()
    p3.start()

if __name__ == '__main__':
    main()