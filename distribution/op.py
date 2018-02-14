#!/usr/bin/env python3
import sys
import os
import logging
import json
import datahandler
from rabbitmq import worker

logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')


# what can be received
# -- hive that needs drones
# { 33 }
# -- hive that needs drones in 3h prediction
# { 33 : 3 }
#def operator(message):
	#hive_id = datahandler.get_hive_id_by(message)
	#if():
	#	demand_based_distribution()
	#elif(message == ):
def main():
	worker.main()


if __name__ == '__main__':
	main()