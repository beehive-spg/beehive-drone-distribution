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