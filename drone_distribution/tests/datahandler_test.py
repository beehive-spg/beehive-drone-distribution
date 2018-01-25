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