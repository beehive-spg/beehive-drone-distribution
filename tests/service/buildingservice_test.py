#!/usr/bin/env python3
from pytest import fixture
from unittest.mock import patch
from distribution.domain.building import Building
from distribution.service import buildingservice

@fixture
def all_buildings():
	return [{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz", "demand": -1}},
			{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
			{"id": 12,"name": "Westbahnhof", "demand": -1}}]

@fixture
def building1():
	return Building({"id": 1,"address": "Karlsplatz",
						"xcoord": 16,"ycoord": 48,"hive":
						{"id": 11,"name": "Karlsplatz", "demand": -1}})

@fixture
def building2():
	return Building({"id": 2,"address": "Westbahnhof",
						"xcoord": 32,"ycoord": 11,"hive":
						{"id": 12,"name": "Westbahnhof", "demand": -1}})

@patch('distribution.rest.rest.get_all_buildings')
def test_get_all_buildings(mock_hives):
	mock_hives.return_value = all_buildings()
	buildings = buildingservice.get_all_buildings()
	expected_buildings = [ building1(), building2() ]
	assert_domain_lists(buildings, expected_buildings)

def test_get_buildingdomain():
	buildingdomain = buildingservice.get_buildingdomain(building1())
	expected_buidling = Building(building1())
	assert buildingdomain.to_primitive() == expected_buidling.to_primitive()

def assert_domain_lists(domains, expected_domains):
	assert len(domains) == len(expected_domains)
	for i in range(len(domains)):
		assert domains[i].to_primitive() == expected_domains[i].to_primitive()