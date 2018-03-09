#!/usr/bin/env python3
import json
from foundation import logger
from distribution.service import buildingservice, routeservice, hiveservice

def update_demand(message):
	decoded_message = message.decode("utf-8")
	loaded_message = json.loads(decoded_message)
	logger.info("Received message: " + str(loaded_message))

	route_id = int(loaded_message['route_id'])
	hop_id = int(loaded_message['hop_id'])

	route = routeservice.get_route_by(route_id)
	hop = routeservice.get_hop_in_route(route, hop_id)

	hives_to_update = get_new_demand(route, hop)
	log_hives = hiveservice.get_json_of_hives(hives_to_update)
	logger.info("Route_ " + str(route_id) +": hives to update " + str(log_hives))

	hiveservice.update_demands(hives_to_update)

def get_in_out_ratio(inc, out):
	return inc / out

def get_new_demand(route, hop_id):
	end_hive = get_end_hop_demand(route, hop_id)

	start_hop = route.hops[0]
	if (is_start_hop(hop_id, start_hop.id)):
		start_hive = get_start_hop_demand(start_hop)
		return [ start_hive, end_hive ]

	return [ end_hive ]

def is_start_hop(message_hop, route_start):
	return message_hop == route_start


def get_start_hop_demand(start_hop):
	start_hive = hiveservice.get_hive_by(start_hop.start.id)
	start_hive.demand = 1
	return start_hive

def get_end_hop_demand(route, hop):
	end_hop = route.hops[len(route.hops)-1]
	endhop_hive = hiveservice.get_hive_by(end_hop.end.id)
	endhop_hive.demand = routeservice.get_route_distance_progress(route, hop)
	return endhop_hive

