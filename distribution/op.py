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
    p4 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p5 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p6 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p7 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p8 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p9 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p10 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p11 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p12 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p13 = Process(target=distribution_consumer.main, args=(distribution_status, queue))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()
    p11.start()
    p12.start()
    p13.start()

if __name__ == '__main__':
    main()