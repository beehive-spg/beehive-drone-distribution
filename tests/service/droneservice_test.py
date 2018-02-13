#!/usr/bin/env python3
from pytest import fixture
from unittest.mock import patch
from distribution.domain.drone import Drone
from distribution.domain.dronetype import Dronetype
from distribution.service import droneservice, locationservice

@fixture
def json_drones():
	return [{"id": 101,"hive": {"id": 11},"name": "drone01",
				"type": {"id": 0},"status": {"ident": "drone.status/idle"}},
			{"id": 102,"hive": {"id": 12},"name": "drone02",
				"type": {"id": 0},"status": {"ident": "drone.status/idle"}},
			{"id": 103,"hive": {"id": 11},"name": "drone03",
				"type": {"id": 0},"status": {"ident": "drone.status/idle"}}]

@fixture
def domain_drones():
	return [Drone({"id": 101,"hive": {"id": 11},"name": "drone01",
				"type": {"id": 0},"status": {"ident": "drone.status/idle"}}),
			Drone({"id": 102,"hive": {"id": 12},"name": "drone02",
				"type": {"id": 0},"status": {"ident": "drone.status/idle"}}),
			Drone({"id": 103,"hive": {"id": 11},"name": "drone03",
				"type": {"id": 0},"status": {"ident": "drone.status/idle"}})]

@fixture
def json_types():
	return {"id": 101, "name": "type-01", "range": 100,
			"speed": 15, "chargetime": 30, "default": True}

@fixture
def typedomain():
	return Dronetype({"id": 101, "name": "type-01", "range": 100,
					"speed": 15, "chargetime": 30, "default": True})

@patch('distribution.rest.rest.get_all_drones')
def test_get_all_drones(mock_drones):
	mock_drones.return_value = json_drones()
	drones = droneservice.get_all_drones()
	expected_drones = [ domain_drones()[0], domain_drones()[1],domain_drones()[2] ]
	assert_domain_lists(drones, expected_drones)

def test_get_dronedomain():
	dronedomain = droneservice.get_dronedomain(domain_drones()[0])
	expected_drone = Drone(domain_drones()[0])
	assert dronedomain.to_primitive() == expected_drone.to_primitive()

@patch('distribution.service.droneservice.get_flying_time')
@patch('distribution.service.droneservice.get_types')
def test_get_time_of_impact(mock_type, mock_flying_time):
	mock_type.return_value = typedomain()
	mock_flying_time.return_value = 3
	time_of_impact = droneservice.get_time_of_impact(0, 0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('distribution.service.droneservice.get_average_flying_time')
@patch('distribution.service.droneservice.get_types')
def test_get_average_time_of_impact(mock_type, mock_flying_time):
	mock_type.return_value = typedomain()
	mock_flying_time.return_value = 3
	time_of_impact = droneservice.get_average_time_of_impact(0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('distribution.service.locationservice.get_average_distance_to')
def test_get_average_flying_time(mock_distance):
	mock_distance.return_value = 150
	flying_time = droneservice.get_average_flying_time(0, typedomain())
	expected_time = 10
	assert flying_time == expected_time

@patch('distribution.service.locationservice.get_distance_between')
def test_get_flying_time(mock_distance):
	mock_distance.return_value = 150
	flying_time = droneservice.get_flying_time(0, 0, typedomain())
	expected_time = 10
	assert flying_time == expected_time

@patch('distribution.rest.rest.get_all_drones')
def test_total_number_of_drones(mock_drones):
	mock_drones.return_value = json_drones()
	number_of_drones = droneservice.get_total_number_of_drones()
	expected_number_of_drones = 3
	assert number_of_drones == expected_number_of_drones

@patch('distribution.rest.rest.get_types')
def test_get_types(mock_types):
	mock_types.return_value = json_types()
	types = droneservice.get_types()
	expected_types = typedomain()
	assert types == expected_types

def assert_domain_lists(domains, expected_domains):
	assert len(domains) == len(expected_domains)
	for i in range(len(domains)):
		assert domains[i].to_primitive() == expected_domains[i].to_primitive()