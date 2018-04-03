#!/usr/bin/env python3
import json
from pytest import fixture
from unittest.mock import patch
from distribution.domain.building import Building
from distribution.service import buildingservice

@fixture
def json_buildings():
	return [{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz", "demand": -1}},
			{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
			{"id": 12,"name": "Westbahnhof", "demand": -1}}]

@fixture
def domain_buildings():
	return [Building({"id": 1,"address": "Karlsplatz",
						"xcoord": 16,"ycoord": 48,"hive":
						{"id": 11,"name": "Karlsplatz", "demand": -1}}),
			Building({"id": 2,"address": "Westbahnhof",
						"xcoord": 32,"ycoord": 11,"hive":
						{"id": 12,"name": "Westbahnhof", "demand": -1}})]

@fixture
def all_reachable():
	return 	[{'id': 1111,'start': {'id': 1},
				'end': {'id': 2},'distance': 3000},
			{'id': 2222,'start': {'id': 3},
				'end': {'id': 1},'distance': 2500},
			{'id': 3333,'start': {'id': 2},
				'end': {'id': 3},'distance': 2800}]

@patch('distribution.rest.rest.get_all_buildings')
def test_get_all_buildings(mock_hives):
	mock_hives.return_value = json_buildings()
	buildings = buildingservice.get_all_buildings()
	expected_buildings = [ domain_buildings()[0], domain_buildings()[1] ]
	assert_domain_lists(buildings, expected_buildings)

def test_get_buildingdomain():
	buildingdomain = buildingservice.get_buildingdomain(domain_buildings()[0])
	expected_buidling = Building(domain_buildings()[0])
	assert buildingdomain.to_primitive() == expected_buidling.to_primitive()

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_reachable_buildings(mock_reachable):
	reachable_buildings = json.dumps(all_reachable())
	mock_reachable.return_value = json.loads(reachable_buildings)
	reachable_buildings = buildingservice.get_reachable_buildings(3)
	expected_buildings = [ 1, 2 ]
	assert reachable_buildings == expected_buildings

def assert_domain_lists(domains, expected_domains):
	assert len(domains) == len(expected_domains)
	for i in range(len(domains)):
		assert domains[i].to_primitive() == expected_domains[i].to_primitive()