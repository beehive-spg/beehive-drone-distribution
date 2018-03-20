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