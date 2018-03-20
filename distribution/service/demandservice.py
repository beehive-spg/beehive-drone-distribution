#!/usr/bin/env python3
import json
from foundation.logger import Logger
from distribution.service import buildingservice, routeservice, hiveservice, distributionservice

logger = Logger(__name__)

def update_demand(message):
	decoded_message = message.decode("utf-8")
	loaded_message = json.loads(decoded_message)
	logger.info("Received message: " + str(loaded_message))

	event_type = loaded_message['type']
	if (event_type == "dep"):
		return
	route_id = int(loaded_message['route_id'])
	hop_id = int(loaded_message['hop_id'])

	route = routeservice.get_route_by(route_id)
	hop = routeservice.get_hop_in_route(route, hop_id)

	hives_to_update = get_new_demand(route, hop)
	logger.info("Route_" + str(route_id))
	for hive in hives_to_update:
		logger.info("Hive to update: " + str(hive.to_primitive()))
	hiveservice.update_demands(hives_to_update)

def get_new_demand(route, hop):
	end_hive = get_end_hop_demand(route, hop)

	start_hop = route.hops[0]
	logger.info("------------------")
	logger.info(start_hop.to_primitive())
	logger.info(hop.to_primitive())
	if (is_start_hop(hop, start_hop)):
		start_hive = get_start_hop_demand(start_hop)
		logger.info("status of route: {}".format(route.origin.ident))
		if (route.origin.ident != "route.origin/distribution"):
			distributionservice.evaluate_hive(start_hive)
		return [ start_hive, end_hive ]

	return [ end_hive ]

def is_start_hop(message_hop, route_start):
	return message_hop.id == route_start.id

def get_start_hop_demand(start_hop):
	start_hive = hiveservice.get_hive_by(start_hop.start.id)
	start_hive.demand = 1
	return start_hive

def get_end_hop_demand(route, hop):
	end_hop = route.hops[len(route.hops)-1]
	endhop_hive = hiveservice.get_hive_by(end_hop.end.id)
	endhop_hive.demand -= routeservice.get_route_distance_progress(route, hop)
	return endhop_hive