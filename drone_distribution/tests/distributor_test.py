#!/usr/bin/env python3
import collections, pytest
from unittest.mock import patch
from drone_distribution import distributor, datahandler

def test_get_ordered_ranking():
	input_ranking = { 33:0.8, 11:0.94, 22:0.2, 1:0.93 }
	output_ranking = distributor.get_ordered_ranking(input_ranking)
	expected_ranking = { 22:0.2, 33:0.8, 1:0.93, 11:0.94 }
	assert output_ranking == expected_ranking

@patch('drone_distribution.datahandler.get_drones_to_send')
def test_get_sending_neighbors_enough_supply(mock_drones_to_send):
	mock_drones_to_send.side_effect = [ 15, 10 ]
	ranking = [ (22,0.2), (33,0.8), (1,0.93), (11,0.94) ]
	ranking = collections.OrderedDict(ranking)
	drones_needed = 20
	sending_drones = distributor.get_sending_neighbors(ranking, drones_needed)
	expected_neighbors = { 22:15, 33:5 }
	assert sending_drones == expected_neighbors

@patch('drone_distribution.distributor.get_neighbor_ranking_of')
@patch('drone_distribution.datahandler.get_drones_to_send')
def test_get_sending_neighbors_not_enough_supply(mock_drones_to_send,
													mock_neighbors):
	mock_drones_to_send.side_effect = [ 10, 5, 1, 1, 5 ]
	neighbors = [ (2,0.2), (77,0.25), (5,0.43), (44,0.5) ]
	neighbors = collections.OrderedDict(neighbors)
	mock_neighbors.return_value = neighbors
	ranking = [ (22,0.2), (33,0.8), (1,0.93), (11,0.94) ]
	ranking = collections.OrderedDict(ranking)
	drones_needed = 20
	sending_drones = distributor.get_sending_neighbors(ranking, drones_needed)
	expected_neighbors = { 22:10, 33:5, 1:1, 11:1 }
	assert sending_drones == expected_neighbors

@patch('drone_distribution.datahandler.get_sum_of_workload_of')
@patch('drone_distribution.datahandler.get_prediction_status')
@patch('drone_distribution.datahandler.get_reachable_hives')
def test_get_neighbor_ranking_of_without_training_weight(
									mock_reachable_hives,
									mock_prediction_status,
									mock_workload_sum):
	mock_reachable_hives.return_value = { 1, 2, 3 }
	mock_prediction_status.side_effect = [ 0.3, -0.1, -0.2 ]
	mock_workload_sum.side_effect = [ 1.9, 1.4, 1.8 ]
	expected_ranking = [ (2, 1.26), (3, 1.44), (1, 2.47) ]
	expected_ranking = collections.OrderedDict(expected_ranking)
	output_ranking = distributor.get_neighbor_ranking_of(0)
	assert expected_ranking == pytest.approx(output_ranking)

@patch('drone_distribution.distributor.get_hive_local_drone_status')
@patch('drone_distribution.datahandler.get_reachable_hives')
def test_get_possible_giving_neighbors(mock_reachable_hives, mock_hive_drones_status):
	mock_reachable_hives.return_value = [ 1, 2, 3, 4, 5 ]
	mock_hive_drones_status.side_effect = [ True, False, False, True, True ]
	neighbors = distributor.get_possible_giving_neighbors(0)
	expected_neighbors = [ 1, 4, 5 ]
	assert neighbors == expected_neighbors

@patch('drone_distribution.distributor.get_hive_local_drone_status')
@patch('drone_distribution.datahandler.get_reachable_hives')
def test_get_possible_receiving_neighbors(mock_reachable_hives, mock_hive_drones_status):
	mock_reachable_hives.return_value = [ 1, 2, 3, 4, 5 ]
	mock_hive_drones_status.side_effect = [ True, False, False, True, True ]
	neighbors = distributor.get_possible_receiving_neighbors(0)
	expected_neighbors = [ 2, 3 ]
	assert neighbors == expected_neighbors

@patch('drone_distribution.distributor.get_local_needed_drones')
@patch('drone_distribution.datahandler.get_url_safe_date_for_the_next_day')
def test_get_hive_local_drone_status_expect_true(mock_date, mock_drones):
	mock_date.return_value = 0
	mock_drones.return_value = 20
	needed_drones = distributor.get_hive_local_drone_status(0)
	expected_drone_status = False
	assert needed_drones == expected_drone_status

@patch('drone_distribution.distributor.get_local_needed_drones')
@patch('drone_distribution.datahandler.get_url_safe_date_for_the_next_day')
def test_get_hive_local_drone_status_expect_false(mock_date, mock_drones):
	mock_date.return_value = 0
	mock_drones.return_value = -20
	needed_drones = distributor.get_hive_local_drone_status(0)
	expected_drone_status = True
	assert needed_drones == expected_drone_status