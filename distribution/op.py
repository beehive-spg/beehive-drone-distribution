#!/usr/bin/env python3
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from distribution.rabbitmq import worker
from pika.exceptions import ConnectionClosed
from distribution.foundation.logger import Logger

logger = Logger(__name__)

def main():
    while(True):
        try:
            worker.main()
        except ConnectionClosed:
            logger.info("RabbitMQ - waiting for connection...")
            time.sleep(5)

if __name__ == '__main__':
    main()