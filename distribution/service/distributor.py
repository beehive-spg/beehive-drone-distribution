#!/usr/bin/env python3
import sys
import os
import logging
from distribution.rabbitmq import publisher
from distribution.service import hiveservice, locationservice, helper
import collections

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')

def start_distribution_to(_id):
	logging.info("distribution process of hive {} has started".format(_id))
	evaluate_conerned_hive(_id)

def evaluate_conerned_hive(_id):
	amount_of_drones = hiveservice.get_amount_of_drones_for(_id)
	logging.info("dist to {}: {} drones needed".format(_id, amount_of_drones))
	neighbor_ranking = get_neighbor_ranking_of(_id)
	logging.info("neighbors: {}".format(neighbor_ranking))
	sending_neighbors = get_sending_neighbors(neighbor_ranking, amount_of_drones)
	logging.info("neighbors sending: {}".format(sending_neighbors))
	publisher.send_distribution(str(sending_neighbors))

def get_neighbor_ranking_of(_id):
	ranking = dict()
	neighbors = hiveservice.get_reachable_hives(_id)
	for neighbor in neighbors:
		multiplier = hiveservice.get_prediction_status(neighbor)
		multiplier += 1
		_sum = hiveservice.get_sum_of_workload_of(neighbor)
		ranking[neighbor] = _sum * multiplier
	return get_ordered_ranking(ranking)

def get_sending_neighbors(ranking, drones_needed):
	sending_neighbors = dict()
	total_available_drones = 0
	for neighbor in ranking:
		drones_left = drones_needed - total_available_drones
		available_drones = hiveservice.get_drones_to_send(neighbor, False)
		if (available_drones > drones_left):
			sending_neighbors[neighbor] = drones_left
			drones_left = 0
			break
		sending_neighbors[neighbor] = available_drones
		total_available_drones += available_drones
	if (drones_left > 0):
		neighbor_rank = get_neighbor_ranking_of(min(ranking, key=ranking.get))
		get_sending_neighbors(neighbor_rank, drones_left)
	return sending_neighbors

def get_ordered_ranking(ranking):
	return collections.OrderedDict(sorted(ranking.items(), key=lambda t: t[1]))

def distribute_inwardly():
	global hives_with_drones
	hives_with_drones = hiveservice.get_hives_with_drones()
	logging.info(hives_with_drones)
	down = locationservice.get_y(descending=True)
	up = locationservice.get_y()
	right = locationservice.get_x()
	left = locationservice.get_x(descending=True)
	logging.info("down"+str(down))
	logging.info(up)
	logging.info(right)
	logging.info(left)
	hives = dict()
	hives_with_location = hiveservice.get_hive_locations()
	if (len(up) < len(right)):
		iterations = len(up)
		logging.info("up is smaller")
	else:
		logging.info("up is smaller")
		iterations = len(right)
	for it in range(iterations):
		hives = locationservice.get_hives_by_y(down[it])
		check_hives(hives)
		hives = locationservice.get_hives_by_x(left[it])
		check_hives(hives)
		hives = locationservice.get_hives_by_y(up[it])
		check_hives(hives)
		hives = locationservice.get_hives_by_x(right[it])
		check_hives(hives)

def check_hives(hives):
	date = helper.get_timestamp_for_the_next_day()
	for hive in hives:
		if (hiveservice.is_giving_drones(hive, date)):
			logging.info("------------------------")
			neighbors = get_possible_receiving_neighbors(hive)
			amount = hiveservice.get_drones_to_send(hive, True)
			send_drones(hive, neighbors, amount)
		else:
			logging.info("-----------------else-")
			neighbors = get_possible_giving_neighbors(hive)
			amount = hiveservice.get_drones_to_send(hive, True)
			receive(neighbors, hive, amount)

def send(_from, to):
	publisher.send_distribution("{ "+str(_from)+":"+str(to)+" }")
	logging.info("from: {} - to: {}".format(_from, to))
	print("from: " + str(_from) + "--- to: " + str(to))
	adjust_number_of_drones_of(_from, to)

def send_drones(_from, to, amount):
	nr_per_hive = amount/len(to)
	if (isinstance(nr_per_hive, float)):
		nr_per_hive = int(nr_per_hive)
		send(_from, to[1])
	for hive in to:
		for nr in nr_per_hive:
			send(_from, hive)

def receive(_from, to, amount):
	nr_per_hive = amount/len(_from)
	if (isinstance(nr_per_hive, float)):
		nr_per_hive = int(nr_per_hive)
		send(_from[1], to)
	for hive in _from:
		for nr in nr_per_hive:
			send(hive, to)

def get_possible_receiving_neighbors(_id):
	possible_neighbors = []
	neighbors = hiveservice.get_reachable_hives(_id)
	for neighbor in neighbors:
		if (not get_hive_local_drone_status(neighbor)):
			possible_neighbors.append(neighbor)
	return possible_neighbors

def get_possible_giving_neighbors(_id):
	logging.info("---------------ölasdfj--")
	possible_giving_neighbors = []
	neighbors = hiveservice.get_reachable_hives(_id)
	logging.info(_id)
	logging.info(neighbors)
	for neighbor in neighbors:
		if (get_hive_local_drone_status(neighbor)):
			possible_giving_neighbors.append(neighbor)
	return possible_giving_neighbors

def adjust_number_of_drones_of(_from, to):
	reduce_drones_of_hive(_from)
	increase_drones_of_hive(to)

def reduce_drones_of_hive(_id):
	hives_with_drones[_id] -= 1

def increase_drones_of_hive(_id):
	hives_with_drones[_id] += 1

def get_local_needed_drones(_id):
	date_of_next_day = helper.get_timestamp_for_the_next_day()
	demand = hiveservice.get_drone_demand(date_of_next_day, _id)
	supply = hives_with_drones[_id]
	return demand - supply

# returns if a hive needs drones or can give drones
# true gives, false needs
def get_hive_local_drone_status(_id):
	number_of_drones = get_local_needed_drones(_id)
	if (number_of_drones > 0):
		return False
	return True