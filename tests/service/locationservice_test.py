#!/usr/bin/env python3
import json
from mock import patch
from unittest import TestCase
from pytest import fixture
from distribution.domain.building import Building
from distribution.rest import rest
from distribution.service import locationservice
from distribution.foundation.exceptions import DomainIdError

@fixture
def domain_buildings():
	return [
				Building({"id": 1,"address": "Karlsplatz",
							"xcoord": 16,"ycoord": 48,
							"hive":{"id": 11,"name": "Karlsplatz",
							"demand": -1, "free": 1}}),
				Building({"id": 2,"address": "Westbahnhof",
							"xcoord": 32,"ycoord": 11,
							"hive":{"id": 12,"name": "Westbahnhof",
							"demand": -1, "free": 3}}),
				Building({"id": 3,"address": "Stephansplatz",
							"xcoord": 2,"ycoord": 21,
							"hive":{"id": 13,"name": "Stephansplatz",
							"demand": -1, "free": 8}})]

@fixture
def json_reachable():
	return [{	"id": 1,"start": {"id": 11},
				"end": {"id": 13},"distance": 3000},
				{"id": 2,"start": {"id": 12},
				"end": {"id": 13},"distance": 2500},
				{"id": 3,"start": {"id": 12},
				"end": {"id": 11},"distance": 2500}]

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_average_distance_to(mock_reachable):
	reachable_buildings = json.dumps(json_reachable())
	mock_reachable.return_value = json.loads(reachable_buildings)
	reachable_buildings = locationservice.get_average_distance_to(13)
	expected_hives = 5500 / 2
	assert reachable_buildings == expected_hives

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_distance_between(mock_reachable):
	reachable_buildings = json.dumps(json_reachable())
	mock_reachable.return_value = json.loads(reachable_buildings)
	distance = locationservice.get_distance_between(12, 13)
	expected_distance = 2500
	assert distance == expected_distance

@patch('distribution.rest.rest.get_reachable_buildings')
def test_get_distance_between_return_error_code(mock_reachable):
	reachable_buildings = json.dumps(json_reachable())
	mock_reachable.return_value = json.loads(reachable_buildings)
	with TestCase.assertRaises(TestCase, DomainIdError) as die:
		locationservice.get_distance_between(12, 14)

def test_get_x_values_descending_false():
	x = locationservice.get_x_values(domain_buildings())
	expected_x = [ 2, 16, 32 ]
	assert x == expected_x

def test_get_x_descending_true():
	x = locationservice.get_x_values(domain_buildings(), True)
	expected_x = [ 32, 16, 2 ]
	assert x == expected_x

def test_get_y_descending_false():
	y = locationservice.get_y_values(domain_buildings())
	expected_y = [ 11, 21, 48 ]
	assert y == expected_y

def test_get_y_descending_true():
	y = locationservice.get_y_values(domain_buildings(), True)
	expected_y = [ 48, 21, 11 ]
	assert y == expected_y

def test_get_hives_by_x():
	hives = locationservice.get_buildings_by_x(2, domain_buildings())
	expected_hives = [ domain_buildings()[2] ]
	assert hives == expected_hives

def test_get_hives_by_y():
	hives = locationservice.get_buildings_by_y(11,domain_buildings())
	expected_hives = [ domain_buildings()[1] ]
	assert hives == expected_hives

def test_get_upper_x():
	x = locationservice.get_upper_x(domain_buildings())
	expected_x = 32
	assert x == expected_x

def test_get_upper_y():
	y = locationservice.get_upper_y(domain_buildings())
	expected_y = 48
	assert y == expected_y

def test_get_lower_x():
	x = locationservice.get_lower_x(domain_buildings())
	expected_x = 2
	assert x == expected_x

def test_get_lower_y():
	y = locationservice.get_lower_y(domain_buildings())
	expected_y = 11
	assert y == expected_y