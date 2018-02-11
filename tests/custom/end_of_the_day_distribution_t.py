#!/usr/bin/env python3
import json, sys, random, os
from mock import patch
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#sys.path.append(os.environ.get('HOMEPATH', os.environ['HOMEPATH'])+"beehive-drone-distribution/")
from drone_distribution import datahandler, distributor, rest, dronehandler

def main():
	setUp()
	test_distribution()
	tearDown()

def setUp():
	hive_ids = datahandler.get_all_hive_ids()
	for hive in hive_ids:
		datahandler.set_drones_for_hive(hive,random.randrange(1, 20))

def test_distribution():
	datahandler.get_drones_of_hive(1)
	datahandler.get_hives_with_drones()
	mock_data()
	distributor.distribute_inwardly()
	print("--- final distribution ---")
	print(datahandler.get_hives_with_drones())

@patch('drone_distribution.datahandler.get_needed_drones')
def mock_data(mock_needed_drones):
	drones_amount = []
	for amount in assign_test_distribution().values():
		drones_amount.append(amount)
	mock_needed_drones.side_effect = drones_amount

def assign_test_distribution():
	all_hives = rest.get_all_hives()
	total_drones = dronehandler.get_total_number_of_drones()
	hives = dict()
	for hive in all_hives:
		if (total_drones > 0):
			drones = int(total_drones / random.randrange(total_drones))
			total_drones -= drones
		hives[hive['hive']['id']] = drones
	print("--- test distribution ---")
	print(hives)
	return hives

def tearDown():
	print("----------------")
	print("RESTART DATABASE")
	print("----------------")

if __name__ == '__main__':
    main()