#!/usr/bin/env python3
import os
import requests as r

def get_reachable_buildings():
	hives = r.get(url("/reachable"))
	return hives.json()

def get_types():
	types = r.get(url("/types"))
	return types.json()

# will be implemented
def get_number_of_moved_drones():
	drones = r.get(url("/distributions"))
	return drones.json()

def get_all_hives():
	hives = r.get(url("/hives"))
	return hives.json()

def get_all_hives_with_workload():
	hives = r.get(url("/hives/workload"))
	return hives.json()

def get_hive_by(_id):
	hive = r.get(url("/one/hive/" + str(_id)))
	return hives.json()

def get_all_drones():
	hives = r.get(url("/drones"))
	return hives.json()

def get_drones_of_hive(_id):
	hives = r.get(url("/drones/hive/" + str(_id)))
	return hives.json()

def post_hive_drone(drone):
	r.post(url("/drones"), json.dumps(drone.to_primitive()))

def post_drone_demand_of_hive(_id, hive):
	r.post(url("/hive/" + json.dumps(hive.to_primitive())))

def url(route):
	host = os.environ.get('DB_URL', os.environ['DBURL'])
	return host + route

# TODO: adapt to database
def get_orders_in(time, _id):
	orders = r.get(url("/hives/workload/:"+str(time)+"/:"+str(_id)))
	return orders.json()

def get_drones_in(time, _id):
	drones = r.get(url("/"))
	return drones.json()

# TODO: adapt to new evaluation model
def get_hive_weight_evaluation():
	evaluation = r.get(url("/"))
	return evaluation.json()

def post_hive_weight(weights):
	r.post(url("/"), str(weights))