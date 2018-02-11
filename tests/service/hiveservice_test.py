#!/usr/bin/env python3
import json
from pytest import fixture
from unittest.mock import patch
from distribution.domain.hive import Hive
from distribution.domain.drone import Drone
from distribution.domain.point import Point
from distribution.service import hiveservice, buildingservice, droneservice

@fixture
def json_buildings():
	return [{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,
			"hive":{"id": 11,"name": "Karlsplatz",
				"demand": -1, "free": 1}},
			{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,
			"hive":{"id": 12,"name": "Westbahnhof",
				"demand": -1, "free": 3}},
			{"id": 3,"address": "Stephansplatz",
			"xcoord": 2,"ycoord": 21,
			"hive":{"id": 13,"name": "Stephansplatz",
				"demand": -1, "free": 8}}]

@fixture
def json_hives():
	return [{"id": 11,"name": "Karlsplatz", "free": 1},
			{"id": 12,"name": "Westbahnhof", "free": 3}]

@fixture
def domain_hives():
	return [Hive({"id": 11,"name": "Karlsplatz", "demand": -1, "free": 1}),
			Hive({"id": 12,"name": "Westbahnhof", "demand": -1, "free": 3}),
			Hive({"id": 13,"name": "Stephansplatz", "demand": -1, "free": 8})]

@fixture
def json_reachable():
	return 	[{'id': 1111,'start': {'id': 1},
				'end': {'id': 2},'distance': 3000},
			{'id': 2222,'start': {'id': 3},
				'end': {'id': 1},'distance': 2500},
			{'id': 3333,'start': {'id': 2},
				'end': {'id': 3},'distance': 2800}]

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

@patch('distribution.service.hiveservice.get_drones_in')
@patch('distribution.service.hiveservice.get_orders_in')
def test_get_workload_in(mock_orders, mock_drones):
	mock_orders.return_value = 10
	mock_drones.return_value = 2
	workload = hiveservice.get_workload_in(1,1)
	assert workload == 5

@patch('distribution.service.droneservice.get_time_of_impact')
@patch('distribution.service.hiveservice.get_drones_in')
@patch('distribution.service.hiveservice.get_orders_in')
@patch('distribution.service.hiveservice.get_workload_in')
def test_amount_of_drones_for(mock_workload, mock_orders,
								mock_drones, mock_impact_time):
	workload = 0.5
	orders = 50
	drones = 100
	mock_workload.return_value = workload
	mock_orders.return_value = orders
	mock_drones.return_value = drones
	mock_impact_time.side_effect = [ 100, 100 ]
	expected_amount = drones - (orders / workload)
	amount_of_drones = hiveservice.get_amount_of_drones_for(0)
	assert amount_of_drones == expected_amount

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_reachable_buildings(mock_reachable):
	reachable_buildings = json.dumps(json_reachable())
	mock_reachable.return_value = json.loads(reachable_buildings)
	reachable_buildings = buildingservice.get_reachable_buildings(3)
	expected_hives = [ 1, 2 ]
	assert reachable_buildings == expected_hives

@patch('distribution.rest.rest.get_drones_in')
def test_get_drones_in(mock_drones):
	mock_drones.return_value = 10
	drones = hiveservice.get_drones_in(1,1)
	assert drones == 10

@patch('distribution.rest.rest.get_orders_in')
def test_orders_in(mock_orders):
	mock_orders.return_value = 10
	orders = hiveservice.get_orders_in(1,1)
	assert orders == 10

def test_get_free_drones():
	free_drones = hiveservice.get_free_drones(12, json_hives())
	expected_drones = 3
	assert free_drones == expected_drones

@patch('distribution.service.droneservice.get_time_of_impact')
@patch('distribution.service.hiveservice.get_workload_in')
def test_get_prediction_status_rising(mock_workload, mock_time_of_impact):
	mock_workload.side_effect = [ int(0.5), int(0.8) ]
	mock_time_of_impact.return_value = 100
	workload = hiveservice.get_prediction_status(1)
	assert workload == int(0.3)

@patch('distribution.service.droneservice.get_time_of_impact')
@patch('distribution.service.hiveservice.get_workload_in')
def test_get_prediction_status_decreasing(mock_workload, mock_time_of_impact):
	mock_workload.side_effect = [ 0.8, 0.5 ]
	mock_time_of_impact.return_value = 100
	workload = hiveservice.get_prediction_status(1)
	assert round(workload, 1) == -0.3

@patch('distribution.service.droneservice.get_time_of_impact')
@patch('distribution.service.hiveservice.get_workload_in')
def test_get_sum_of_workload(mock_workload, mock_impact_time):
	workloads = [ 0.5, 0.6, 0.7 ]
	mock_workload.side_effect = workloads
	mock_impact_time.side_effect = [ 10, 10 ]
	_sum = hiveservice.get_sum_of_workload_of(0)
	expected_sum = workloads[0] + workloads[1] + workloads[2]
	assert _sum == expected_sum

@patch('distribution.service.hiveservice.get_needed_drones')
def test_get_drones_to_send_eotd_true(mock_needed_drones):
	mock_needed_drones.return_value = 10
	needed_drones = hiveservice.get_drones_to_send(1, True)
	assert needed_drones == 10

@patch('distribution.service.hiveservice.get_free_drones')
@patch('distribution.rest.rest.get_all_buildings')
def test_get_drones_to_send_eotd_false(mock_buildings, mock_free_drones):
	mock_buildings.return_value = ""
	mock_free_drones.return_value = 10
	drones_without_impact = hiveservice.get_drones_to_send(1, False)
	assert drones_without_impact == 10

@patch('distribution.service.hiveservice.get_needed_drones')
def test_is_giving_drones_return_true(mock_drones):
	mock_drones.return_value = 20
	status = hiveservice.is_giving_drones(0, 0)
	expected_status = True
	assert status == expected_status

@patch('distribution.service.hiveservice.get_needed_drones')
def test_is_giving_drones_return_false(mock_drones):
	mock_drones.return_value = -20
	status = hiveservice.is_giving_drones(0, 0)
	expected_status = False
	assert status == expected_status

@patch('distribution.service.hiveservice.get_free_drones')
@patch('distribution.service.hiveservice.get_drone_demand')
def test_get_needed_drones_positive(mock_demand, mock_supply):
	mock_demand.return_value = 20
	mock_supply.return_value = 10
	drones = hiveservice.get_needed_drones(0, 0)
	expected_drones = 10
	assert drones == expected_drones

@patch('distribution.service.hiveservice.get_free_drones')
@patch('distribution.service.hiveservice.get_drone_demand')
def test_get_needed_drones_negative(mock_demand, mock_supply):
	mock_demand.return_value = 10
	mock_supply.return_value = 20
	drones = hiveservice.get_needed_drones(0, 0)
	expected_drones = -10
	assert drones == expected_drones

@patch('distribution.service.droneservice.get_all_drones')
def test_get_drones_of_hive(mock_drones):
	mock_drones.return_value = domain_drones()
	drones = hiveservice.get_drones_of_hive(11)
	expected_drones = [ domain_drones()[0], domain_drones()[2] ]
	assert_domain_lists(drones, expected_drones)

@patch('distribution.rest.rest.get_all_buildings')
def test_get_all_hive_ids(mock_buildings):
	mock_buildings.return_value = json_buildings()
	hives = hiveservice.get_all_hive_ids()
	expected_hives = [ 11, 12, 13 ]
	assert hives == expected_hives

@patch('distribution.rest.rest.get_all_drones')
@patch('distribution.service.hiveservice.get_all_hives')
def test_get_hives_with_dronecount(mock_hives, mock_drones):
	mock_hives.return_value = domain_hives()
	mock_drones.return_value = json_drones()
	hives_with_drones = hiveservice.get_hives_with_dronecount()
	expected_hives_with_drones = { 11:2, 12:1 }
	expected_length = len(expected_hives_with_drones)
	length = 0
	for hive in hives_with_drones:
		if (hive in expected_hives_with_drones):
			if (hives_with_drones[hive] == expected_hives_with_drones[hive]):
				length += 1
	assert length == expected_length

@patch('distribution.rest.rest.get_all_buildings')
def test_get_all_hives(mock_buildings):
	mock_buildings.return_value = json_buildings()
	hives = hiveservice.get_all_hives()
	hive11 = domain_hives()[0]
	hive12 = domain_hives()[1]
	hive13 = domain_hives()[2]
	expected_hives = [ hive11, hive12, hive13 ]
	assert_domain_lists(hives, expected_hives)

def test_get_hivedomain():
	hive = {"id": 11,"name": "Karlsplatz", "demand": -1}
	hivedomain = hiveservice.get_hivedomain(hive)
	expected_hivedomain = Hive(hive)
	assert hivedomain.to_primitive() == expected_hivedomain.to_primitive()

def assert_domain_lists(domains, expected_domains):
	assert len(domains) == len(expected_domains)
	for i in range(len(domains)):
		assert domains[i].to_primitive() == expected_domains[i].to_primitive()