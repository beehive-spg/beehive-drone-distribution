import sys
sys.path.insert(0, '../rabbitmq/consumer/')
from worker import Worker
import threading

worker = Worker('workload_prediction_queue')
worker.start()