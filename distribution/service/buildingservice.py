#!/usr/bin/env python3
from distribution.domain.building import Building
from distribution.rest import rest

def get_all_buildings():
	all_buildings = rest.get_all_buildings()
	buildings = []
	for building in all_buildings:
		buildingdomain = get_buildingdomain(building)
		buildings.append(buildingdomain)
	return buildings

def get_buildingdomain(json):
	building = Building(json)
	building.validate()
	return building