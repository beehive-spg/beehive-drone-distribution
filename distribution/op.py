#!/usr/bin/env python3
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from multiprocessing import Process, Pipe
from distribution.rabbitmq import distribution_consumer
from distribution.rabbitmq import settings_consumer
from pika.exceptions import ConnectionClosed
from distribution.foundation.logger import Logger

logger = Logger(__name__)

def main():
    distribution_status = 0 #off
    parent_conn, child_conn = Pipe()
    p1 = Process(target=settings_consumer.main, args=(distribution_status, child_conn))
    p2 = Process(target=distribution_consumer.main, args=(distribution_status, parent_conn))
    p1.start()
    p2.start()

if __name__ == '__main__':
    main()