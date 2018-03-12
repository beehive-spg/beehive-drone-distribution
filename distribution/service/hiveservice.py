#!/usr/bin/env python3
import json
from distribution.domain.hive import Hive
from distribution.domain.drone import Drone
from distribution.domain.building import Building
from distribution.rest import rest
from distribution.service import buildingservice, droneservice, helper
from distribution.foundation.exceptions import domain_id_error

def get_drone_demand(hiveid, hives):
	for hive in hives:
		if (hive.id == hiveid):
			return hive.demand
	raise domain_id_error("Hive", hiveid)

def get_free_drones(hive):
	number_of_drones = len(get_drones_of_hive(hive.id))
	incoming = get_number_of_incoming_hops(hive.id)
	outgoing = get_number_of_outgoing_hops(hive.id)
	return number_of_drones - outgoing + incoming - hive.demand

def get_free_drones_of_hive(hiveid, hives):
	for hive in hives:
		hive = Hive(hive)
		if (hive.id == hiveid):
			return hive.free
	raise domain_id_error("Hive", hiveid)

def update_demand(hive):
	rest.put_demand_of(hive)

def update_demands(hives):
	for hive in hives:
		update_demand(hive)

def get_number_of_incoming_hops(hiveid):
	buildingid = get_building_of_hive(hiveid).id
	incoming_hops = buildingservice.get_number_of_incoming_hops(buildingid)
	return incoming_hops

def get_number_of_outgoing_hops(hiveid):
	buildingid = get_building_of_hive(hiveid).id
	outgoing_hops = buildingservice.get_number_of_incoming_hops(buildingid)
	return outgoing_hops

def get_io_ratio(hive):
	return get_number_of_incoming_hops / get_number_of_outgoing_hops

# TODO: maybe change to rest route
def get_building_of_hive(hiveid):
	buildings = buildingservice.get_all_buildings()
	for building in buildings:
		if (building.hive.id == hiveid):
			return building
	raise domain_id_error("Hive", hiveid)

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

def get_all_hives():
	all_buildings = buildingservice.get_all_buildings()
	hives = []
	for building in all_buildings:
		hives.append(building.hive)
	return hives

def get_all_hives_by_buildings(buildings):
	all_buildings = buildings
	hives = []
	for building in all_buildings:
		hives.append(building.hive)
	return hives

def get_hivedomain(json):
	hive = Hive(json)
	hive.validate()
	return hive

def get_hive_by(buildingid):
	all_buildings = buildingservice.get_all_buildings()
	for building in all_buildings:
		if (building.id == buildingid):
			return building.hive
	raise domain_id_error(buildingid)

def get_json_of_hives(hives):
	hive_primitives = []
	for hive in hives:
		hive_primitives.append(hive.to_primitive())
	return hive_primitives

def get_number_of_hives():
	return len(get_all_hives())

def get_reachable_hives(hiveid):
	building = get_building_of_hive(hiveid)
	reachable_buildings = buildingservice.get_reachable_buildings(building.id)
	reachable_hives = []
	for buildingid in reachable_buildings:
		hive = get_hive_by(buildingid)
		reachable_hives.append(hive)
	return reachable_hives


### TESTING
def set_drones_for_hive(hiveid, amount):
	for nr in range(amount):
		drone = Drone()
		drone.hive.id = hiveid
		drone.name = "drone-"+str(nr)
		drone.status.ident = "drone.status/idle"
		rest.post_hive_drone(drone)

### ---------------------------------------- OPTIONAL

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

def is_giving_drones_now(hiveid):
	return get_free_drones(hiveid, helper.now())

def is_giving_drones(hiveid, time):
	number_of_drones = get_needed_drones(hiveid, time)
	if (number_of_drones > 0):
		return True
	return False