#!/usr/bin/env python3
import json
from unittest.mock import patch
from drone_distribution import datahandler
from drone_distribution.point import Point

@patch('drone_distribution.datahandler.get_drones_in')
@patch('drone_distribution.datahandler.get_orders_in')
def test_get_workload_in(mock_orders, mock_drones):
	mock_orders.return_value = 10
	mock_drones.return_value = 2
	workload = datahandler.get_workload_in(1,1)
	assert workload == 5

@patch('drone_distribution.datahandler.get_time_of_impact')
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

@patch('drone_distribution.datahandler.get_chargetime_of_drone')
@patch('drone_distribution.datahandler.get_average_flying_time')
def test_get_average_time_of_impact(mock_flying_time, mock_charge_time):
	mock_flying_time.return_value = 3
	mock_charge_time.return_value = 30
	time_of_impact = datahandler.get_average_time_of_impact(0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('drone_distribution.datahandler.get_chargetime_of_drone')
@patch('drone_distribution.datahandler.get_flying_time')
def test_get_time_of_impact(mock_flying_time, mock_charge_time):
	mock_flying_time.return_value = 3
	mock_charge_time.return_value = 30
	time_of_impact = datahandler.get_time_of_impact(0, 0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('drone_distribution.datahandler.get_speed_of_drone')
@patch('drone_distribution.datahandler.get_average_distance_to')
def test_get_average_flying_time(mock_distance, mock_speed):
	mock_distance.return_value = 150
	mock_speed.return_value = 15
	flying_time = datahandler.get_average_flying_time(0, 0)
	expected_time = 10
	assert flying_time == expected_time

@patch('drone_distribution.datahandler.get_speed_of_drone')
@patch('drone_distribution.datahandler.get_distance_between')
def test_get_flying_time(mock_distance, mock_speed):
	mock_distance.return_value = 150
	mock_speed.return_value = 15
	flying_time = datahandler.get_flying_time(0, 0, 0)
	expected_time = 10
	assert flying_time == expected_time

@patch('drone_distribution.rest.get_reachable_hives')
def test_get_reachable_hives(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 13},
					'end': {'id': 12},'distance': 2500},
					{'id': 3,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_hives = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_hives)
	reachable_hives = datahandler.get_reachable_hives(13)
	expected_hives = [ 11, 12 ]
	assert reachable_hives == expected_hives

@patch('drone_distribution.rest.get_reachable_hives')
def test_get_average_distance_to(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 12},
					'end': {'id': 13},'distance': 2500},
					{'id': 3,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_hives = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_hives)
	reachable_hives = datahandler.get_average_distance_to(13)
	expected_hives = 5500 / 2
	assert reachable_hives == expected_hives

@patch('drone_distribution.rest.get_reachable_hives')
def test_get_distance_between(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 12},
					'end': {'id': 13},'distance': 2500},
					{'id': 3,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_hives = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_hives)
	distance = datahandler.get_distance_between(12, 13)
	expected_distance = 2500
	assert distance == expected_distance

@patch('drone_distribution.rest.get_reachable_hives')
def test_get_distance_between_return_error_code(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_hives = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_hives)
	distance = datahandler.get_distance_between(12, 13)
	expected_distance = -1
	assert distance == expected_distance

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

@patch('drone_distribution.datahandler.get_time_of_impact')
@patch('drone_distribution.datahandler.get_workload_in')
def test_get_prediction_status_rising(mock_workload, mock_time_of_impact):
	mock_workload.side_effect = [ int(0.5), int(0.8) ]
	mock_time_of_impact.return_value = 100
	workload = datahandler.get_prediction_status(1)
	assert workload == int(0.3)

@patch('drone_distribution.datahandler.get_time_of_impact')
@patch('drone_distribution.datahandler.get_workload_in')
def test_get_prediction_status_decreasing(mock_workload, mock_time_of_impact):
	mock_workload.side_effect = [ 0.8, 0.5 ]
	mock_time_of_impact.return_value = 100
	workload = datahandler.get_prediction_status(1)
	assert round(workload, 1) == -0.3

@patch('drone_distribution.datahandler.get_time_of_impact')
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
def test_get_drones_to_send_eotd_false(mock_free_drones):
	mock_free_drones.return_value = 10
	drones_without_impact = datahandler.get_drones_to_send(1, False)
	assert drones_without_impact == 10

@patch('drone_distribution.datahandler.get_needed_drones')
def test_get_hive_drone_status_return_true(mock_drones):
	mock_drones.return_value = 20
	status = datahandler.get_hive_drone_status(0, 0)
	expected_status = True
	assert status == expected_status

@patch('drone_distribution.datahandler.get_needed_drones')
def test_get_hive_drone_status_return_false(mock_drones):
	mock_drones.return_value = -20
	status = datahandler.get_hive_drone_status(0, 0)
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

@patch('drone_distribution.datahandler.get_hive_locations')
def test_get_x_descending_false(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	x = datahandler.get_x()
	expected_x = [ 1, 2, 3, 5 ]
	assert x == expected_x

@patch('drone_distribution.datahandler.get_hive_locations')
def test_get_x_descending_true(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	x = datahandler.get_x(True)
	expected_x = [ 5, 3, 2, 1 ]
	assert x == expected_x

@patch('drone_distribution.datahandler.get_hive_locations')
def test_get_y_descending_false(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	y = datahandler.get_y()
	expected_y = [ 1, 3, 5, 8 ]
	assert y == expected_y

@patch('drone_distribution.datahandler.get_hive_locations')
def test_get_y_descending_true(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	y = datahandler.get_y(True)
	expected_y = [ 8, 5, 3, 1 ]
	assert y == expected_y

@patch('drone_distribution.datahandler.get_hive_locations')
def test_get_hives_by_x(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(2,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	hives = datahandler.get_hives_by_x(2)
	expected_hives = [ 2, 3 ]
	assert hives == expected_hives

@patch('drone_distribution.datahandler.get_hive_locations')
def test_get_hives_by_y(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,1), 3:Point(3,5), 4:Point(5,1) }
	mock_hive_locations.return_value = locations
	hives = datahandler.get_hives_by_y(1)
	expected_hives = [ 1, 2, 4 ]
	assert hives == expected_hives

@patch('drone_distribution.datahandler.get_hive_locations')
def test_get_map_border(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(5,8), 3:Point(3,5), 4:Point(2,3) }
	mock_hive_locations.return_value = locations
	map_border = datahandler.get_map_border()
	expected_border = [ 8, 5, 1, 1 ]
	assert map_border == expected_border

@patch('drone_distribution.rest.get_all_hives')
def test_get_hive_locations(mock_all_hives):
	all_hives = [
		{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz"}},
		{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
		{"id": 12,"name": "Westbahnhof"}
		}]
	mock_all_hives.return_value = all_hives
	hives = datahandler.get_hive_locations()
	expected_hives = { 1:Point(16,48), 2:Point(32,11) }
	assert len(hives) == len(expected_hives)

@patch('drone_distribution.rest.get_drones_of_hive')
def test_get_hives_with_drones(mock_drones_of_hives):
	drones_of_hive = [
	{"id": 1,"name": "drone01","type": {"id": 17592186045434},
		"status": {"id": 17592186045421}},
    {"id": 2,"name": "drone02","type": {"id": 17592186045434},
    	"status": {"id": 17592186045421}}]
	mock_drones_of_hives.return_value = drones_of_hive
	drones = datahandler.get_drones_of_hive(0)
	expected_drones = [ 1, 2 ]
	assert drones == expected_drones

@patch('drone_distribution.rest.get_all_hives')
def test_get_all_hive_ids(mock_all_hives):
	all_hives = [
		{"id": 1,"address": "Karlsplatz",
			"xcoord": 16,"ycoord": 48,"hive":
			{"id": 11,"name": "Karlsplatz"}},
		{"id": 2,"address": "Westbahnhof",
			"xcoord": 32,"ycoord": 11,"hive":
		{"id": 12,"name": "Westbahnhof"}
		}]
	mock_all_hives.return_value = all_hives
	hives = datahandler.get_all_hive_ids()
	expected_hives = [ 11, 12 ]
	assert hives == expected_hives