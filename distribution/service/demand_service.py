#!/usr/bin/env python3
import sys
import logging
from distribution.service import buildingservice

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
	format='%(asctime)s - %(name)-5s- %(levelname)-5s- %(message)s')

def update_demand(message):
	buildings = buildingservice.get_all_buildings(message)
	hives = hiveservice.get_all_hives_by_buildings(buidlings)
	for hive in hives:
		hive.incoming = hiveservice.get_incoming_drones(hive.id, hives)
		hive.outgoing = hiveservice.get_outgoing_drones(hive.id, hives)
		#get_in_out_ratio(hive.incoming, hive.outgoing)
		#update demand of domains
		hive.demand = get_new_demand(hive)
	hiveservice.update_demand(hives)

def get_in_out_ratio(inc, out):
	return inc / out

def get_new_demand(hivedomain):
	# io_ratio
	# free
	# if free is minus, then check for (free) neighbor distribution
	# instead of or in addition to updating demand
	demand = hivedomain.demand
	new_demand = 10
	return new_demand