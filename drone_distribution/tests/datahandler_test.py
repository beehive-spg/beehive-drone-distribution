#!/usr/bin/env python3
import json
from unittest.mock import patch
from drone_distribution.point import Point
from drone_distribution import datahandler
from drone_distribution import dronehandler

@patch('drone_distribution.datahandler.get_drones_in')
@patch('drone_distribution.datahandler.get_orders_in')
def test_get_workload_in(mock_orders, mock_drones):
	mock_orders.return_value = 10
	mock_drones.return_value = 2
	workload = datahandler.get_workload_in(1,1)
	assert workload == 5

@patch('drone_distribution.dronehandler.get_time_of_impact')
@patch('drone_distribution.datahandler.get_drones_in')
@patch('drone_distribution.datahandler.get_orders_in')
@patch('drone_distribution.datahandler.get_workload_in')
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
	amount_of_drones = datahandler.get_amount_of_drones_for(0)
	assert amount_of_drones == expected_amount

@patch('drone_distribution.rest.get_reachable_buildings')
def test_get_reachable_buildings(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 13},
					'end': {'id': 12},'distance': 2500},
					{'id': 3,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_buildings = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_buildings)
	reachable_buildings = datahandler.get_reachable_buildings(13)
	expected_hives = [ 11, 12 ]
	assert reachable_buildings == expected_hives

@patch('drone_distribution.rest.get_reachable_buildings')
@patch('drone_distribution.rest.get_all_hives')
def test_get_reachable_hives(mock_hives, mock_reachable):
	all_hives = [	{"id": 1,"address": "Karlsplatz",
					"xcoord": 16,"ycoord": 48,"hive":{
					"id": 11,"name": "Karlsplatz"}},
					{"id": 2,"address": "Westbahnhof",
					"xcoord": 32,"ycoord": 11,"hive":{
					"id": 12,"name": "Westbahnhof"}},
					{"id": 3,"address": "Westbahnhof",
					"xcoord": 32,"ycoord": 11,"hive":{
					"id": 13,"name": "Westbahnhof"}}]
	mock_hives.return_value = all_hives
	reachable = [	{'id': 1111,'start': {'id': 1},
					'end': {'id': 2},'distance': 3000},
					{'id': 2222,'start': {'id': 3},
					'end': {'id': 1},'distance': 2500},
					{'id': 3333,'start': {'id': 2},
					'end': {'id': 3},'distance': 2800}]
	reachable_buildings = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_buildings)
	reachable_hives = datahandler.get_reachable_hives(12)
	expected_hives = [ 11, 13 ]
	assert reachable_hives == expected_hives

@patch('drone_distribution.rest.get_drones_in')
def test_get_drones_in(mock_drones):
	mock_drones.return_value = 10
	drones = datahandler.get_drones_in(1,1)
	assert drones == 10

@patch('drone_distribution.rest.get_orders_in')
def test_orders_in(mock_orders):
	mock_orders.return_value = 10
	orders = datahandler.get_orders_in(1,1)
	assert orders == 10

def test_get_free_drones():
	all_hives = [
		{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz", "free": 1}},
		{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
		{"id": 12,"name": "Westbahnhof", "free": 3}
		}]
	free_drones = datahandler.get_free_drones(2, all_hives)
	expected_drones = 3
	assert free_drones == expected_drones

@patch('drone_distribution.dronehandler.get_time_of_impact')
@patch('drone_distribution.datahandler.get_workload_in')
def test_get_prediction_status_rising(mock_workload, mock_time_of_impact):
	mock_workload.side_effect = [ int(0.5), int(0.8) ]
	mock_time_of_impact.return_value = 100
	workload = datahandler.get_prediction_status(1)
	assert workload == int(0.3)

@patch('drone_distribution.dronehandler.get_time_of_impact')
@patch('drone_distribution.datahandler.get_workload_in')
def test_get_prediction_status_decreasing(mock_workload, mock_time_of_impact):
	mock_workload.side_effect = [ 0.8, 0.5 ]
	mock_time_of_impact.return_value = 100
	workload = datahandler.get_prediction_status(1)
	assert round(workload, 1) == -0.3

@patch('drone_distribution.dronehandler.get_time_of_impact')
@patch('drone_distribution.datahandler.get_workload_in')
def test_get_sum_of_workload(mock_workload, mock_impact_time):
	workloads = [ 0.5, 0.6, 0.7 ]
	mock_workload.side_effect = workloads
	mock_impact_time.side_effect = [ 10, 10 ]
	_sum = datahandler.get_sum_of_workload_of(0)
	expected_sum = workloads[0] + workloads[1] + workloads[2]
	assert _sum == expected_sum

@patch('drone_distribution.datahandler.get_needed_drones')
def test_get_drones_to_send_eotd_true(mock_needed_drones):
	mock_needed_drones.return_value = 10
	needed_drones = datahandler.get_drones_to_send(1, True)
	assert needed_drones == 10

@patch('drone_distribution.datahandler.get_free_drones')
@patch('drone_distribution.rest.get_all_hives')
def test_get_drones_to_send_eotd_false(mock_hives, mock_free_drones):
	mock_hives.return_value = ""
	mock_free_drones.return_value = 10
	drones_without_impact = datahandler.get_drones_to_send(1, False)
	assert drones_without_impact == 10

@patch('drone_distribution.datahandler.get_needed_drones')
def test_is_giving_drones_return_true(mock_drones):
	mock_drones.return_value = 20
	status = datahandler.is_giving_drones(0, 0)
	expected_status = True
	assert status == expected_status

@patch('drone_distribution.datahandler.get_needed_drones')
def test_is_giving_drones_return_false(mock_drones):
	mock_drones.return_value = -20
	status = datahandler.is_giving_drones(0, 0)
	expected_status = False
	assert status == expected_status

@patch('drone_distribution.datahandler.get_drone_supply')
@patch('drone_distribution.datahandler.get_drone_demand')
def test_get_needed_drones_positive(mock_demand, mock_supply):
	mock_demand.return_value = 20
	mock_supply.return_value = 10
	drones = datahandler.get_needed_drones(0, 0)
	expected_drones = 10
	assert drones == expected_drones

@patch('drone_distribution.datahandler.get_drone_supply')
@patch('drone_distribution.datahandler.get_drone_demand')
def test_get_needed_drones_negative(mock_demand, mock_supply):
	mock_demand.return_value = 10
	mock_supply.return_value = 20
	drones = datahandler.get_needed_drones(0, 0)
	expected_drones = -10
	assert drones == expected_drones

@patch('drone_distribution.rest.get_all_hives')
def test_get_hive_locations(mock_hives):
	all_hives = [
		{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz"}},
		{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
		{"id": 12,"name": "Westbahnhof"}
		}]
	mock_hives.return_value = all_hives
	hives = datahandler.get_hive_locations()
	expected_hives = { 1:Point(16,48), 2:Point(32,11) }
	assert len(hives) == len(expected_hives)

@patch('drone_distribution.rest.get_drones_of_hive')
def test_get_drones_of_hive(mock_drones_of_hive):
	drones_of_hive = [
		{"id": 1,"name": "drone01","type": {"id": 17592186045434},
			"status": {"id": 17592186045421}},
		{"id": 2,"name": "drone02","type": {"id": 17592186045434},
			"status": {"id": 17592186045421}}]
	mock_drones_of_hive.return_value = drones_of_hive
	drones = datahandler.get_drones_of_hive(0)
	expected_drones = [ 1, 2 ]
	assert drones == expected_drones

@patch('drone_distribution.rest.get_all_hives')
def test_get_all_hive_ids(mock_hives):
	all_hives = [
		{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz"}},
		{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
		{"id": 12,"name": "Westbahnhof"}
		}]
	mock_hives.return_value = all_hives
	hives = datahandler.get_all_hive_ids()
	expected_hives = [ 11, 12 ]
	assert hives == expected_hives

@patch('drone_distribution.rest.get_all_drones')
@patch('drone_distribution.rest.get_all_hives')
def test_get_hives_with_drones(mock_hives, mock_drones):
	all_hives = [
		{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz"}},
		{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
			{"id": 12,"name": "Westbahnhof"}
		}]
	all_drones = [
		{"id": 101,"hive": {"id": 11},"name": "drone01",
			"type": {"id": 0},"status": {"ident": "IDLE"}},
		{"id": 102,"hive": {"id": 12},"name": "drone02",
			"type": {"id": 0},"status": {"ident": "IDLE"}},
		{"id": 103,"hive": {"id": 11},"name": "drone03",
			"type": {"id": 0},"status": {"ident": "IDLE"}
		}]
	mock_hives.return_value = all_hives
	mock_drones.return_value = all_drones
	hives_with_drones = datahandler.get_hives_with_drones()
	expected_hives_with_drones = { 11:2, 12:1 }
	expected_length = len(expected_hives_with_drones)
	length = 0
	for hive in hives_with_drones:
		if (hive in expected_hives_with_drones):
			if (hives_with_drones[hive] == expected_hives_with_drones[hive]):
				length += 1
	assert length == expected_length