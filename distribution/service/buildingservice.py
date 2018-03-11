#!/usr/bin/env python3
from distribution.domain.building import Building
from distribution.domain.reachable import Reachable
from distribution.rest import rest

def get_all_buildings():
	all_buildings = rest.get_all_buildings()
	buildings = []
	for building in all_buildings:
		buildingdomain = get_buildingdomain(building)
		buildings.append(buildingdomain)
	return buildings

def get_all_buildings_in(buildings):
	all_buildings = buildings
	buildings = []
	for building in all_buildings:
		buildingdomain = get_buildingdomain(building)
		buildings.append(buildingdomain)
	return buildings

def get_buildingdomain(json):
	building = Building(json)
	building.validate()
	return building

def get_reachable_buildings(buildingid):
	reachable_buildings = rest.get_reachable_buildings()
	reachable = []
	for reach in reachable_buildings:
		reachabledomain = Reachable(reach)
		if (reachabledomain.start.id == buildingid):
			reachable.append(reachabledomain.end.id)
		elif (reachabledomain.end.id == buildingid):
			reachable.append(reachabledomain.start.id)
	return reachable

def get_number_of_incoming_hops(buildingid):
	return len(rest.get_incoming_hops)

def get_number_of_outgoing_hops(buildingid):
	return len(rest.get_outgoing_hops)