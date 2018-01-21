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

def distribute_inwardly():
	down = datahandler.get_y().sort(reverse=True)
	up = datahandler.get_y()
	right = datahandler.get_x()
	left = datahandler.get_x().sort(reverse=True)
	hives = dict()
	hives_with_location = datahandler.get_hive_locations_by_id()
	if (len(up) < len(right)):
		iterations = len(up)
	else:
		iterations = len(right)
	for it in iterations:
		hives = datahandler.get_hive_y(down[it])
		check_hives(hives)
		hives = datahandler.get_hive_x(left[it])
		check_hives(hives)
		hives = datahandler.get_hive_y(up[it])
		check_hives(hives)
		hives = datahandler.get_hive_x(right[it])
		check_hives(hives)

def check_hives(hives):
	for hive in hives:
		if (not hive.get_hive_drone_status(hive, 60)):
			send(hive, datahanddler.get_possible_neighbors(), datahandler.get_drones_to_send(hive, True))
		else:
			receive(datahandler.get_possible_giving_neighbors(), hive)

def send(_from, to):
	publisher.send("{ "+str(_from)+":"+str(to)+" }")

def send(_from, to, amount):
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

def get_possible_neighbors(_id):
	possible_neighbors = []
	neighbors = datahandler.get_neighborhood_from(_id)
	for neighbor in neighbors:
		if (datahandler.get_hive_drone_status(neighbor, 60)):
			possible_neighbors.append(hive)
	return possible_neighbors

def get_possible_giving_neighbors(_id):
	possible_giving_neighbors = []
	neighbors = datahandler.get_neighborhood_from(_id)
	for neighbor in neighbors:
		if (not datahandler.get_hive_drone_status(neighbor, 60)):
			possible_giving_neighbors.append(hive)
	return possible_giving_neighbors