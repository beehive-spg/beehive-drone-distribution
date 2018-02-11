#!/usr/bin/env python3
import json
from mock import patch
from distribution.domain.point import Point
from distribution.rest import rest
from distribution.service import locationservice, locationservice

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_average_distance_to(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 12},
					'end': {'id': 13},'distance': 2500},
					{'id': 3,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_buildings = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_buildings)
	reachable_buildings = locationservice.get_average_distance_to(13)
	expected_hives = 5500 / 2
	assert reachable_buildings == expected_hives

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_distance_between(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 12},
					'end': {'id': 13},'distance': 2500},
					{'id': 3,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_buildings = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_buildings)
	distance = locationservice.get_distance_between(12, 13)
	expected_distance = 2500
	assert distance == expected_distance

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_distance_between_return_error_code(mock_reachable):
	reachable = [{	'id': 1,'start': {'id': 11},
					'end': {'id': 13},'distance': 3000},
					{'id': 2,'start': {'id': 12},
					'end': {'id': 11},'distance': 2500}]
	reachable_buildings = json.dumps(reachable)
	mock_reachable.return_value = json.loads(reachable_buildings)
	distance = locationservice.get_distance_between(12, 13)
	expected_distance = -1
	assert distance == expected_distance

@patch('distribution.service.hiveservice.get_hive_locations')
def test_get_map_border(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(5,8), 3:Point(3,5), 4:Point(2,3) }
	mock_hive_locations.return_value = locations
	map_border = locationservice.get_map_border()
	expected_border = [ 8, 5, 1, 1 ]
	assert map_border == expected_border

@patch('distribution.service.hiveservice.get_hive_locations')
def test_get_x_descending_false(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	x = locationservice.get_x()
	expected_x = [ 1, 2, 3, 5 ]
	assert x == expected_x

@patch('distribution.service.hiveservice.get_hive_locations')
def test_get_x_descending_true(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	x = locationservice.get_x(True)
	expected_x = [ 5, 3, 2, 1 ]
	assert x == expected_x

@patch('distribution.service.hiveservice.get_hive_locations')
def test_get_y_descending_false(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	y = locationservice.get_y()
	expected_y = [ 1, 3, 5, 8 ]
	assert y == expected_y

@patch('distribution.service.hiveservice.get_hive_locations')
def test_get_y_descending_true(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(3,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	y = locationservice.get_y(True)
	expected_y = [ 8, 5, 3, 1 ]
	assert y == expected_y

@patch('distribution.service.hiveservice.get_hive_locations')
def test_get_hives_by_x(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,8), 3:Point(2,5), 4:Point(5,3) }
	mock_hive_locations.return_value = locations
	hives = locationservice.get_hives_by_x(2)
	expected_hives = [ 2, 3 ]
	assert hives == expected_hives

@patch('distribution.service.hiveservice.get_hive_locations')
def test_get_hives_by_y(mock_hive_locations):
	locations = { 1:Point(1,1), 2:Point(2,1), 3:Point(3,5), 4:Point(5,1) }
	mock_hive_locations.return_value = locations
	hives = locationservice.get_hives_by_y(1)
	expected_hives = [ 1, 2, 4 ]
	assert hives == expected_hives

def test_get_upper_x():
	locations = { 1:Point(1,1), 2:Point(2,1), 3:Point(5,6), 4:Point(5,0) }
	x = locationservice.get_upper_x(locations)
	expected_x = 5
	assert x == expected_x

def test_get_upper_y():
	locations = { 1:Point(1,1), 2:Point(2,1), 3:Point(5,6), 4:Point(5,0) }
	y = locationservice.get_upper_y(locations)
	expected_y = 6
	assert y == expected_y

def test_get_lower_x():
	locations = { 1:Point(1,1), 2:Point(2,1), 3:Point(5,6), 4:Point(5,0) }
	x = locationservice.get_lower_x(locations)
	expected_x = 1
	assert x == expected_x

def test_get_lower_y():
	locations = { 1:Point(1,1), 2:Point(2,1), 3:Point(5,6), 4:Point(5,0) }
	y = locationservice.get_lower_y(locations)
	expected_y = 0
	assert y == expected_y