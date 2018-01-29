#!/usr/bin/env python3
from unittest.mock import patch
from drone_distribution import datahandler, test_requests

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

@patch('drone_distribution.test_requests.request_charging_time')
@patch('drone_distribution.test_requests.request_flying_time')
def test_get_time_of_impact(mock_flying_time, mock_charging_time):
	mock_flying_time.return_value = 3
	mock_charging_time.return_value = 30
	time_of_impact = datahandler.get_time_of_impact()
	expected_time = 33
	assert time_of_impact == expected_time

@patch('drone_distribution.test_requests.request_drones_in')
def test_get_drones_in(mock_drones):
	mock_drones.return_value = 10
	drones = datahandler.get_drones_in(1,1)
	assert drones == 10

@patch('drone_distribution.test_requests.request_orders_in')
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

@patch('drone_distribution.datahandler.get_drones_without_impact')
def test_get_drones_to_send_eotd_false(mock_drones_without_impact):
	mock_drones_without_impact.return_value = 10
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