#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from distribution.rabbitmq import worker

print("test")
worker.main()
print("test")