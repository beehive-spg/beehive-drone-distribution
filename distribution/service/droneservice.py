#!/usr/bin/env python3
from distribution.rest import rest
from distribution.domain.dronetype import Dronetype
from distribution.domain.drone import Drone
from distribution.service import locationservice

def get_all_drones():
	all_drones = rest.get_all_drones()
	drones = []
	for drone in all_drones:
		dronedomain = get_dronedomain(drone)
		drones.append(dronedomain)
	return drones

def get_time_of_impact(_from, to):
	types = get_types()
	flying_time = get_flying_time(_from, to, types)
	return flying_time + types.chargetime

# TODO: get remaining charging time
def get_average_time_of_impact(_id):
	types = get_types()
	flying_time = get_average_flying_time(_id, types)
	return flying_time + types.chargetime

def get_flying_time(_from, to, types):
	distance = locationservice.get_distance_between(_from, to)
	return distance / types.speed

def get_average_flying_time(_id, types):
	distance = locationservice.get_average_distance_to(_id)
	return distance / types.speed

def get_total_number_of_drones():
	all_drones = rest.get_all_drones()
	return len(all_drones)

def get_dronedomain(json):
	drone = Drone(json)
	drone.validate()
	return drone

def get_types():
	types = rest.get_types()
	typedomain = Dronetype(types)
	return typedomain