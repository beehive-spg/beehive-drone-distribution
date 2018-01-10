#!/usr/bin/env python3
import random

def request_orders_in(time, _id):
	return random.randrange(20, 90)

def request_drones_in(time, _id):
	return 100

def request_neighborhood_hives(_id):
	return [11,22,33,44]

def request_flying_time():
	return 40

def request_charging_time():
	return 20

def request_available_drones(_id):
	return random.randrange(0, 20)

def request_average_workload():
	return 50

def request_hive_weight_evaluation():
	return random.randrange()

def request_number_of_moved_drones():
	return random.randrange(150, 250)

def request_all_hives():
	return [10,20,30,40,50,60,70,80]