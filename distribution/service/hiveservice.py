#!/usr/bin/env python3
import json
from distribution.domain.hive import Hive
from distribution.domain.drone import Drone
from distribution.domain.building import Building
from distribution.rest import rest
from distribution.service import buildingservice, droneservice, helper

# eotd true, returns drones needed for the next day
# eotd false, returns drones needed to harm the network as little as possible
def get_drones_to_send(hiveid, eotd):
	if (eotd):
		return get_needed_drones(hiveid, helper.get_timestamp_for_the_next_day())
	hives = rest.get_all_buildings()
	return get_free_drones(hiveid, hives)

# returns number of drones needed(+) or missing(-)
def get_needed_drones(hiveid, time):
	demand = get_drone_demand(time, hiveid)
	supply = get_free_drones(time, hiveid)
	return demand - supply

def get_drone_demand(hiveid, hives):
	for hive in hives:
		if (hive.id == hiveid):
			return hive.demand
	return 99999

# TODO: adapt to database
# TODO: non existing id? possible?
def get_free_drones(hiveid, hives):
	for hive in hives:
		hive = Hive(hive)
		if (hive.id == hiveid):
			return hive.free
	return -1

def set_d_of_hive(hiveid, hives):
	incoming = get_incoming_drones(hiveid, hives)
	outgoing = get_outgoing_drones(hiveid, hives)
	io_ratio = incoming / outgoing
	drone_demand = get_drone_demand(hiveid, hives)
	get_hivedomain(hives)
	hive = Hive()
	hive.id = hiveid
	hive.demand = drone_demand
	rest.post_desired_drones_of_hive(hive)

# TODO: error code handling, parameter is list of hives
def get_incoming_drones(hiveid, hives):
	for hive in hives:
		if (hive.id == hiveid):
			return hive.incoming
	return 99999

def get_outgoing_drones(hiveid, hives):
	for hive in hives:
		if (hive.id == hiveid):
			return hive.outgoing
	return 99999

def get_building_of_hive(hiveid):
	buildings = buildingservice.get_all_buildings()
	for building in buildings:
		if (building.hive.id == hiveid):
			return building.id
	return -1

def is_giving_drones_now(hiveid):
	return is_giving_drones(hiveid, helper.now())

def is_giving_drones(hiveid, time):
	number_of_drones = get_needed_drones(hiveid, time)
	if (number_of_drones > 0):
		return True
	return False

def get_all_hive_ids():
	all_hives = get_all_hives()
	hives = []
	for h in all_hives:
		hive = Hive(h)
		hives.append(hive.id)
	return hives

def get_drones_of_hive(hiveid):
	all_drones = droneservice.get_all_drones()
	drones = []
	for drone in all_drones:
		if (drone.hive.id == hiveid):
			drones.append(drone)
	return drones

def get_hives_with_dronecount():
	all_drones = droneservice.get_all_drones()
	all_hives = get_all_hives()
	hives = dict()
	for hive in all_hives:
		number_of_drones = 0
		for drone in all_drones:
			if (hive.id == drone.hive.id):
				number_of_drones += 1
		hives[hive.id] = number_of_drones
	return hives

#for testing purposes
def set_drones_for_hive(hiveid, amount):
	for nr in range(amount):
		drone = Drone()
		drone.hive.id = hiveid
		drone.name = "drone-"+str(nr)
		drone.status.ident = "drone.status/idle"
		rest.post_hive_drone(drone)

def get_all_hives():
	all_buildings = buildingservice.get_all_buildings()
	hives = []
	for building in all_buildings:
		hives.append(building.hive)
	return hives

def get_hivedomain(json):
	hive = Hive(json)
	hive.validate()
	return hive


### --------- Adapt to database
def get_workload_in(time, hiveid):
	orders = get_orders_in(time, hiveid)
	drones = get_drones_in(time, hiveid)
	return orders / drones

def get_amount_of_drones_for(hiveid):
	workload = get_workload_in(0, hiveid)
	orders = get_orders_in(droneservice.get_time_of_impact(), hiveid)
	drones = get_drones_in(droneservice.get_time_of_impact(), hiveid)
	return drones - (orders / workload)

# rising or decreasing
def get_prediction_status(hiveid):
	current_workload = get_workload_in(0, hiveid)
	predicted_workload = get_workload_in(droneservice.get_time_of_impact(), hiveid)
	return predicted_workload - current_workload

def get_sum_of_workload_of(hiveid):
	current_workload = get_workload_in(0, hiveid)
	_sum = current_workload
	predicted_workload_inbetween = get_workload_in(droneservice.get_time_of_impact()/2, hiveid)
	_sum += predicted_workload_inbetween
	predicted_workload_at_drone_arrival = get_workload_in(droneservice.get_time_of_impact(), hiveid)
	_sum += predicted_workload_at_drone_arrival
	return _sum

# TODO: adapt to database
def get_drones_in(time, hiveid):
	drones = rest.get_drones_in(time, hiveid)
	return drones

# TODO: adapt to database
def get_orders_in(time, hiveid):
	return rest.get_orders_in(time, hiveid)


# TODO: replace by get reachable building if not needed
# TODO: if needed, get_building_of_hive will return buildingdomain
def get_reachable_hives(hiveid):
	hiveid = get_building_of_hive(hiveid)
	buildings = get_reachable_buildings(hiveid)
	all_hives = rest.get_all_hives()
	reachable = []
	for hive in all_hives:
		for building in buildings:
			if (hive['id'] == building):
				reachable.append(hive['hive']['id'])
	return reachable

### ---------------------------------------- OPTIONAL
def get_impact_to(hiveid, drones):
	future_orders = get_orders_in(droneservice.get_time_of_impact(), hiveid)
	future_drones = get_drones_in(droneservice.get_time_of_impact(), hiveid)
	future_drones += drones
	return future_orders / future_drones

def get_hive_weight_evaluation():
	#weight_evaluation = database connection
	return weight_evaluation

def get_number_of_hives():
	return len(get_all_hives())