#!/usr/bin/env python3
from unittest.mock import patch
from drone_distribution import dronehandler, datahandler, locationhandler

@patch('drone_distribution.dronehandler.get_chargetime_of_drone')
@patch('drone_distribution.dronehandler.get_flying_time')
def test_get_time_of_impact(mock_flying_time, mock_charge_time):
	mock_flying_time.return_value = 3
	mock_charge_time.return_value = 30
	time_of_impact = dronehandler.get_time_of_impact(0, 0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('drone_distribution.dronehandler.get_chargetime_of_drone')
@patch('drone_distribution.dronehandler.get_average_flying_time')
def test_get_average_time_of_impact(mock_flying_time, mock_charge_time):
	mock_flying_time.return_value = 3
	mock_charge_time.return_value = 30
	time_of_impact = dronehandler.get_average_time_of_impact(0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('drone_distribution.dronehandler.get_speed_of_drone')
@patch('drone_distribution.locationhandler.get_average_distance_to')
def test_get_average_flying_time(mock_distance, mock_speed):
	mock_distance.return_value = 150
	mock_speed.return_value = 15
	flying_time = dronehandler.get_average_flying_time(0, 0)
	expected_time = 10
	assert flying_time == expected_time

@patch('drone_distribution.dronehandler.get_speed_of_drone')
@patch('drone_distribution.locationhandler.get_distance_between')
def test_get_flying_time(mock_distance, mock_speed):
	mock_distance.return_value = 150
	mock_speed.return_value = 15
	flying_time = dronehandler.get_flying_time(0, 0, 0)
	expected_time = 10
	assert flying_time == expected_time