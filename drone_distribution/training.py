## what i wanna do

# have a list of hives with weights
# { id: weight }

# running the system with test data
# evaluate the number of moved drones
# change weights and evaluate if it helped the system to develop
# --> reducing the number of moved drones


#!/usr/bin/env python3
import logging
import random
import sys
from drone_distribution import test_requests as tr

logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')

def main(accurracy):
	setup_training()
	logging.info("starting training")
	train(accurracy)

def setup_training():
	global moved_drones_before, weighted_hives, changed_hive, flagged_hives
	changed_hive = None
	# retrieve the list of hives with weights
	weighted_hives = { 11:1.1, 22:1.0}
	logging.info("list of hives: " + str(weighted_hives))
	# run system
	moved_drones_before = tr.request_number_of_moved_drones()
	logging.info("number of moved drones before: " + str(moved_drones_before))

def train(accurracy):
	while (len(flagged_hives) != len(weighted_hives)):
		adjust_weights(accurracy)
		# run the whole system with the test data
		logging.info("training completed")
		moved_drones_after = tr.request_number_of_moved_drones()
		movde_drones = get_moved_drones(moved_drones_after)
		logging.info("difference: " + str(movde_drones))
		if (movde_drones > 0):
			number_of_moved_drones = get_moved_drones(moved_drones_after)
			logging.info("training improved by: " + str(number_of_moved_drones))
			reset_flagged_hives()
		elif (changed_hive != None):
			weighted_hives[changed_hive] -= accurracy
			flagged_hives.append(changed_hive)
			logging.info("rollback weight change")
			if (len(flagged_hives) == len(weighted_hives)):
			logging.info("no more training necessary")
			break;

def adjust_weights(accurracy):
	# list with hives which weight changes didn't improve the system
	flagged_hives = {22}
	range_of_hives = len(weighted_hives)
	possible_hives = get_possible_hives()
	random_hive = random.randrange(len(possible_hives))
	weighted_hives[random_hive] += accurracy
	changed_hive = random_hive

def get_moved_drones(after):
	return after - moved_drones_before

def get_possible_hives():
	possible_hives = []
	for hive in weighted_hives:
		if (hive not in flagged_hives):
			possible_hives.append(hive)
	return possible_hives

def reset_flagged_hives():
	flagged_hives = []