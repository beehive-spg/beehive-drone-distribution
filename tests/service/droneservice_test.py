#!/usr/bin/env python3
from unittest.mock import patch
from distribution.service import droneservice, hiveservice, locationservice

@patch('distribution.service.droneservice.get_chargetime_of_drone')
@patch('distribution.service.droneservice.get_flying_time')
@patch('distribution.rest.rest.get_types')
def test_get_time_of_impact(mock_types, mock_flying_time, mock_charge_time):
	mock_types.return_value = ""
	mock_flying_time.return_value = 3
	mock_charge_time.return_value = 30
	time_of_impact = droneservice.get_time_of_impact(0, 0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('distribution.service.droneservice.get_chargetime_of_drone')
@patch('distribution.service.droneservice.get_average_flying_time')
@patch('distribution.rest.rest.get_types')
def test_get_average_time_of_impact(mock_types, mock_flying_time, mock_charge_time):
	mock_types.return_value = ""
	mock_flying_time.return_value = 3
	mock_charge_time.return_value = 30
	time_of_impact = droneservice.get_average_time_of_impact(0)
	expected_time = 33
	assert time_of_impact == expected_time

@patch('distribution.service.droneservice.get_speed_of_drone')
@patch('distribution.service.locationservice.get_average_distance_to')
def test_get_average_flying_time(mock_distance, mock_speed):
	mock_distance.return_value = 150
	mock_speed.return_value = 15
	flying_time = droneservice.get_average_flying_time(0, 0)
	expected_time = 10
	assert flying_time == expected_time

@patch('distribution.service.droneservice.get_speed_of_drone')
@patch('distribution.service.locationservice.get_distance_between')
def test_get_flying_time(mock_distance, mock_speed):
	mock_distance.return_value = 150
	mock_speed.return_value = 15
	flying_time = droneservice.get_flying_time(0, 0, 0)
	expected_time = 10
	assert flying_time == expected_time

@patch('distribution.rest.rest.get_all_drones')
def test_total_number_of_drones(mock_drones):
	drones = [
    {"id": 17592186045921,"hive": {"id": 17592186045486},
	    "name": "drone-10","type":{"name": "large"},
	    "status": {"ident": "IDLE"}},
    {"id": 17592186045923,"hive": {"id": 17592186045486},
    	"name": "drone-11","type": {"name": "large"},
    	"status": {"ident": "IDLE"}},
    {"id": 17592186045925,"hive": {"id": 17592186045486},
    	"name": "drone-12","type": {"name": "large"},
    	"status": {"ident": "IDLE"}}]
	mock_drones.return_value = drones
	number_of_drones = droneservice.get_total_number_of_drones()
	expected_number_of_drones = 3
	assert number_of_drones == expected_number_of_drones