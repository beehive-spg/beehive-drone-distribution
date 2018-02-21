#!/usr/bin/env python3
import sys
import os
import logging
from distribution.service import distributor
from distribution.rabbitmq import worker

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')


print("test")
worker.main()
print("test")