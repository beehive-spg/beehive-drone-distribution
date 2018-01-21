# each hive has an individual weight
# after running the system with test data
# evaluate the number of moved drones
# change weights and evaluate if it helped the system to improve
# --> reducing the number of moved drones as far as possible

#!/usr/bin/env python3
import logging
import random
import sys
from drone_distribution import test_requests as tr

logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')

def main(accuracy):
	setup_training()
	logging.info("starting training")
	train(accuracy)

def setup_training():
	global moved_drones_before, weighted_hives, changed_hive, flagged_hives
	changed_hive = None
	flagged_hives = {22}
	# retrieve the list of hives with weights
	weighted_hives = { 11:1.1, 22:1.0}
	logging.info("list of hives: " + str(weighted_hives))
	# run system
	moved_drones_before = tr.request_number_of_moved_drones()
	logging.info("number of moved drones before: " + str(moved_drones_before))

def train(accuracy, iterations=None):
	iteration = 0
	logging.info("start training iteration: " + iteration +
					"with accuracy: " + accuracy)
	while (len(flagged_hives) != len(weighted_hives) or iteration < iterations):
		logging.info("adjusting weights of hives")
		adjust_weights(accuracy)
		logging.info("start training data")
		# run the whole system with the test data
		logging.info("training data completed")
		moved_drones_after = tr.request_number_of_moved_drones()
		moved_drones = get_moved_drones_difference(moved_drones_after)
		if (moved_drones > 0):
			logging.info("improved by: " + str(moved_drones))
			commit()
		elif (changed_hive != None):
			rollback(changed_hive)
		iteration += 1

def adjust_weights(accuracy):
	# list with hives which weight changes didn't improve the system
	possible_hives = get_possible_hives()
	random_hive = random.randrange(len(possible_hives))
	weighted_hives[random_hive] += accuracy
	changed_hive = random_hive

def commit():
	logging.info("commit weight change")
	# database connection to save weights
	logging.info("reset flagged hives")
	reset_flagged_hives()

def rollback(changed_hive):
	logging.info("rollback weight change")
	weighted_hives[changed_hive] -= accuracy
	flagged_hives.append(changed_hive)

def get_moved_drones_difference(after):
	return after - moved_drones_before

def get_possible_hives():
	possible_hives = []
	for hive in weighted_hives:
		if (hive not in flagged_hives):
			possible_hives.append(hive)
	return possible_hives

def reset_flagged_hives():
	flagged_hives = []