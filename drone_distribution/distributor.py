#!/usr/bin/env python3
import sys
import os
import logging
from drone_distribution import datahandler
from rabbitmq import publisher
import collections

logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')

def start_distribution_to(_id):
	logging.info("distribution process of hive {} has started".format(_id))
	evaluate_conerned_hive(_id)

def evaluate_conerned_hive(_id):
	amount_of_drones = datahandler.get_amount_of_drones_for(_id)
	logging.info("dist to {}: {} drones needed".format(_id, amount_of_drones))
	neighbor_ranking = get_neighbor_ranking_of(_id)
	logging.info("neighbors: {}".format(neighbor_ranking))
	sending_neighbors = get_sending_neighbors(neighbor_ranking, amount_of_drones)
	logging.info("neighbors sending: {}".format(sending_neighbors))
	publisher.send_distribution(str(sending_neighbors))

# we want the lowest ranking hives
# ranks the list of neighbors by summing their workload
# multiply by raising/decreasing factor
# if negative, take the positive value (-0.5 becomes 0.5)
# if positive take the value and add 1 (0.5 becomes 1.5)
# lowest to highest
#####
# loops through list, predicts impact, if the hive ranking would change
# places with the next one, it starts taking drones from next list entry
def get_neighbor_ranking_of(_id):
	ranking = dict()
	neighbors = datahandler.get_neighborhood_from(_id)
	for neighbor in neighbors:
		multiplier = datahandler.get_prediction_status(neighbor)
		multiplier += 1
		_sum = datahandler.get_sum_of_workload_of(neighbor)
		ranking[neighbor] = _sum * multiplier
	return get_ordered_ranking(ranking)

def get_sending_neighbors(ranking, drones_needed):
	sending_neighbors = dict()
	total_available_drones = 0
	for neighbor in ranking:
		drones_left = drones_needed - total_available_drones
		available_drones = datahandler.get_drones_to_send(neighbor, False)
		if (available_drones > drones_left):
			sending_neighbors[neighbor] = drones_left
			break
		sending_neighbors[neighbor] = available_drones
		total_available_drones += available_drones
	return sending_neighbors

def get_ordered_ranking(ranking):
	return collections.OrderedDict(sorted(ranking.items(), key=lambda t: t[1]))

# ideas
# searching for needing hives and getting from their surrounding
# searching hives with too much drones and search for surrounded needing hives
# randomly send from having to needing
def prepare_for_the_next_day():
	hives = datahandler.get_all_hives()
	for hive in hives:
		if (datahandler.get_hive_drone_staus()):
			amount_of_drones = datahandler.get_drones_to_send(_id, True)
			logging.info("EOTD dist to {}: {} drones needed".format(_id, amount_of_drones))
			neighbors = get_possible_neighbors(_id)
			logging.info("EOTD possible neighbors: {}".format(neighbor_ranking))
			sending_neighbors = get_sending_neighbors(neighbors, amount_of_drones)
			logging.info("EOTD neighbors sending: {}".format(sending_neighbors))
			if (not sending_neighbors):
				needing_hives.append(hive)
			else:
				# TODO check sending format, dict should be okay
				publisher.send_distribution(str(sending_neighbors))
	if(needing_hives):
		for needing_hive in needing_hives:
			

def get_possible_neighbors(_id):
	possible_neighbors = []
	neighbors = datahandler.get_neighborhood_from(_id)
	for neighbor in neighbors:
		if (datahandler.get_hive_drone_status()):
			possible_neighbors.append(hive)
	return possible_neighbors