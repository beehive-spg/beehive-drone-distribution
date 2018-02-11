#!/usr/bin/env python3
from unittest.mock import patch
from distribution.domain.building import Building
from distribution.service import buildingservice

@patch('distribution.rest.rest.get_all_buildings')
def test_get_all_buildings(mock_hives):
	all_hives = [
		{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz", "demand": -1}},
		{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
			{"id": 12,"name": "Westbahnhof", "demand": -1}
		}]
	mock_hives.return_value = all_hives
	buildings = buildingservice.get_all_buildings()
	building1 = Building({"id": 1,"address": "Karlsplatz",
						"xcoord": 16,"ycoord": 48,"hive":
						{"id": 11,"name": "Karlsplatz", "demand": -1}})
	building2 = Building({"id": 2,"address": "Westbahnhof",
						"xcoord": 32,"ycoord": 11,"hive":
						{"id": 12,"name": "Westbahnhof", "demand": -1}})
	expected_buildings = [ building1, building2 ]
	assert_two_domain_lists(buildings, expected_buildings)

def test_get_buildingdomain():
	building = {"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz", "demand": -1}}
	buildingdomain = buildingservice.get_buildingdomain(building)
	expected_buidling = Building(building)
	assert buildingdomain.to_primitive() == expected_buidling.to_primitive()

def assert_two_domain_lists(domain1, domain2):
	assert len(domain1) == len(domain2)
	for i in range(len(domain1)):
		assert domain1[i].to_primitive() == domain2[i].to_primitive()