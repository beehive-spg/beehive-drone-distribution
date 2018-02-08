#!/usr/bin/env python3
from drone_distribution import rest, locationhandler

def get_time_of_impact(_from, to):
	types = rest.get_types()
	flying_time = get_flying_time(_from, to, types)
	chargetime = get_chargetime_of_drone(types)
	return flying_time + chargetime

# TODO: get remaining charging time
def get_average_time_of_impact(_id):
	types = rest.get_types()
	flying_time = get_average_flying_time(_id, types)
	chargetime = get_chargetime_of_drone(types)
	return flying_time + chargetime

def get_flying_time(_from, to, types):
	distance = locationhandler.get_distance_between(_from, to)
	speed = get_speed_of_drone(types)
	return distance / speed

def get_average_flying_time(_id, types):
	distance = locationhandler.get_average_distance_to(_id)
	speed = get_speed_of_drone(types)
	return distance / speed

def get_chargetime_of_drone(types):
	return types['chargetime']

def get_speed_of_drone(types):
	return types['speed']

def get_range_of_drone(types):
	return types['range']

def get_total_number_of_drones():
	all_drones = rest.get_all_drones()
	return len(all_drones)