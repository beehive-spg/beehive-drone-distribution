import sys
sys.path.insert(0, '../')
from worker import Worker

worker = Worker()
worker.start_queue()
worker.start_channel()


