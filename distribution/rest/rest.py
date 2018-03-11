#!/usr/bin/env python3
import os
import requests as r
from distribution.service import helper, locationservice

def get_reachable_buildings():
	hives = r.get(url("/api/reachable"))
	hives.raise_for_status()
	return hives.json()

def get_types():
	types = r.get(url("/types"))
	types.raise_for_status()
	return types.json()

def get_to_building(hiveid):
	hives = r.get(url("/api/tobuilding/" + str(hive.id)))
	hives.raise_for_status()
	return hives.json()

def get_incoming_hops(buildingid):
	time = helper.now() + locationservice.get_max_travel_time()
	hives = r.get(url("/hives/incoming/" + str(hive.id) + "/"
						+ str(time)))
	hives.raise_for_status()
	return hives.json()

def get_incoming_hops(buildingid):
	time = helper.now() + locationservice.get_max_travel_time()
	hives = r.get(url("/hives/incoming/" + str(hive.id) + "/"
						+ str(time)))
	hives.raise_for_status()
	return hives.json()

def get_number_of_outgoing_between(hive, start, end):
	hives = r.get(url("/api/outgoing/" + str(hive.id) + "/"
						+ str(start)+ "/" + str(end)))
	hives.raise_for_status()
	return hives.json()

def get_all_buildings():
	hives = r.get(url("/hives"))
	hives.raise_for_status()
	return hives.json()

def get_all_routes():
	routes = r.get(url("/routes"))
	routes.raise_for_status()
	return routes.json()

def get_all_hives_with_workload():
	hives = r.get(url("/hives/workload"))
	hives.raise_for_status()
	return hives.json()

def get_hive_by(_id):
	hive = r.get(url("/one/hive/" + str(_id)))
	hives.raise_for_status()
	return hive.json()

def get_all_drones():
	hives = r.get(url("/drones"))
	hives.raise_for_status()
	return hives.json()

def get_drones_of_hive(_id):
	hives = r.get(url("/hives/" + str(_id) + "/drones"))
	hives.raise_for_status()
	return hives.json()

def post_hive_drone(drone):
	postdrone = dict()
	postdrone['hiveid'] = drone.hive.id
	postdrone['name'] = drone.name
	postdrone['status'] = drone.status.ident
	post = r.post(url("/drones"), json.dumps(postdrone))
	post.raise_for_status()

def put_demand_of(hive):
	put = r.put(url("/hives/" + str(hive.id) + "/" + str(hive.demand)))
	print(put)
	put.raise_for_status()

def url(route):
	host = os.environ.get('DB_URL', os.environ['DBURL'])
	return host + route

# will be implemented
def get_number_of_moved_drones():
	drones = r.get(url("/distributions"))
	drones.raise_for_status()
	return drones.json()