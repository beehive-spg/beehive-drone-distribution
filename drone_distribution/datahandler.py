#!/usr/bin/env python3
import json
import drone_distribution.test_requests as tr
from drone_distribution import rest, helper, dronehandler
from drone_distribution.point import Point

def get_workload_in(time, _id):
	orders = get_orders_in(time, _id)
	drones = get_drones_in(time, _id)
	return orders / drones

def get_amount_of_drones_for(_id):
	workload = get_workload_in(0, _id)
	orders = get_orders_in(dronehandler.get_time_of_impact(), _id)
	drones = get_drones_in(dronehandler.get_time_of_impact(), _id)
	return drones - (orders / workload)

# rising or decreasing
def get_prediction_status(_id):
	current_workload = get_workload_in(0, _id)
	predicted_workload = get_workload_in(dronehandler.get_time_of_impact(), _id)
	return predicted_workload - current_workload

def get_sum_of_workload_of(_id):
	current_workload = get_workload_in(0, _id)
	_sum = current_workload
	predicted_workload_inbetween = get_workload_in(dronehandler.get_time_of_impact()/2, _id)
	_sum += predicted_workload_inbetween
	predicted_workload_at_drone_arrival = get_workload_in(dronehandler.get_time_of_impact(), _id)
	_sum += predicted_workload_at_drone_arrival
	return _sum

# TODO: adapt to database
def get_drones_in(time, _id):
	drones = rest.get_drones_in(time, _id)
	return drones

# TODO: adapt to database
def get_orders_in(time, _id):
	return rest.get_orders_in(time, _id)

# eotd true, returns drones needed for the next day
# eotd false, returns drones needed to harm the network as little as possible
def get_drones_to_send(_id, eotd):
	hives = rest.get_all_hives()
	if (eotd):
		return get_needed_drones(_id, helper.get_timestamp_for_the_next_day())
	return get_free_drones(_id, hives)

# TODO: adapt to database
# TODO: non existing id? possible?
def get_free_drones(_id, hives):
	for hive in hives:
		if (hive['id'] == _id):
			return hive['free']
	return -1

# TODO: refactor
def get_reachable_buildings(_id):
	reachable_buildings = rest.get_reachable_buildings()
	reachable = []
	for hive in reachable_buildings:
		if (hive['start']['id'] == _id):
			reachable.append(hive['end']['id'])
		elif (hive['end']['id'] == _id):
			reachable.append(hive['start']['id'])
	return reachable

def get_reachable_hives(_id):
	buildings = get_reachable_buildings(_id)
	all_hives = rest.get_all_hives()
	reachable = []
	for hive in all_hives:
		for building in buildings:
			if (hive['id'] == building):
				reachable.append(hive['hive']['id'])
	return reachable

def is_giving_drones_now(_id):
	return is_giving_drones(_id, datetime.datetime.now())

def is_giving_drones(_id, time):
	number_of_drones = get_needed_drones(_id, time)
	if (number_of_drones > 0):
		return True
	return False

# returns number of drones needed(+) or missing(-)
def get_needed_drones(_id, time):
	demand = get_drone_demand(time, _id)
	supply = get_drone_supply(time, _id)
	return demand - supply

# returns dict with ids and coordinates
def get_hive_locations():
	all_hives = rest.get_all_hives()
	hives = dict()
	for hive in all_hives:
		hives[hive['id']] = Point(hive['xcoord'], hive['ycoord'])
	return hives;

def get_all_hive_ids():
	all_hives = rest.get_all_hives()
	hives = []
	for hive in all_hives:
		hives.append(hive['hive']['id'])
	return hives

def get_drones_of_hive(_id):
	drones_of_hive = rest.get_drones_of_hive(_id)
	hives = []
	for hive in drones_of_hive:
		hives.append(hive['id'])
	return hives

def get_hives_with_drones():
	all_drones = rest.get_all_drones()
	all_hives = rest.get_all_hives()
	hives = dict()
	for hive in all_hives:
		number_of_drones = 0
		for drone in all_drones:
			if (hive['hive']['id'] == drone['hive']['id']):
				number_of_drones += 1
		hives[hive['hive']['id']] = number_of_drones
	return hives

#for testing purposes
def set_drones_for_hive(hiveid, amount):
	#drones = []
	for nr in range(amount):
		drone = dict()
		drone['hiveid'] = hiveid
		drone['name'] = "drone-"+str(nr)
		drone['status'] = ":status/IDLE"
		#drones.append(drone)
		rest.post_hive_drone(json.dumps(drone, ensure_ascii=False))


### ---------------------------------------- OPTIONAL

def get_impact_to(_id, drones):
	future_orders = get_orders_in(dronehandler.get_time_of_impact(), _id)
	future_drones = get_drones_in(dronehandler.get_time_of_impact(), _id)
	future_drones += drones
	return future_orders / future_drones

def get_hive_weight_evaluation():
	#weight_evaluation = database connection
	return weight_evaluation

def get_number_of_hives():
	return len(get_all_hives())

# TODO: adapt to new model
def get_drone_demand(time, _id):
	return 5

def get_drone_supply(time, _id):
	return tr.request_drones_in(time, _id)