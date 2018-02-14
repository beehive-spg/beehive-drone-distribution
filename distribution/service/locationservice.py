import sys
from distribution.rest import rest
from distribution.service import hiveservice

def get_average_distance_to(hiveid):
	reachable_buildings = rest.get_reachable_buildings()
	distance = []
	for hive in reachable_buildings:
		if (hive['end']['id'] == hiveid or hive['start']['id'] == hiveid):
			distance.append(hive['distance'])
	return sum(distance) / len(distance)

# error code -1 ? possible?
def get_distance_between(_from, to):
	reachable_buildings = rest.get_reachable_buildings()
	for hive in reachable_buildings:
		start = hive['start']['id']
		if (start == _from or start == to):
			end = hive['end']['id']
			if (end == _from or end == to):
				return hive['distance']
	return -1

def get_x_values(all_buildings, descending=False):
	x_values = []
	for building in all_buildings:
		x_values.append(building.xcoord)
	x_values.sort(reverse=descending)
	return x_values

def get_y_values(all_buildings, descending=False):
	y_values = []
	for building in all_buildings:
		y_values.append(building.ycoord)
	y_values.sort(reverse=descending)
	return y_values

def get_buildings_by_x(x, all_buildings):
	x_buildings = []
	buildings = all_buildings
	for building in buildings:
		if (building.xcoord == x):
			x_buildings.append(building)
	return x_buildings

def get_buildings_by_y(y, all_buildings):
	y_buildings = []
	buildings = all_buildings
	for building in buildings:
		if (building.ycoord == y):
			y_buildings.append(building)
	return y_buildings

def get_upper_x(all_buildings):
	x = -1
	for building in all_buildings:
		if (x < building.xcoord):
			x = building.xcoord
	return x

def get_upper_y(all_buildings):
	y = -1
	for building in all_buildings:
		if (y < building.ycoord):
			y = building.ycoord
	return y

def get_lower_x(all_buildings):
	x = sys.maxsize
	for building in all_buildings:
		if (x > building.xcoord):
			x = building.xcoord
	return x

def get_lower_y(all_buildings):
	y = sys.maxsize
	for building in all_buildings:
		if (y > building.ycoord):
			y = building.ycoord
	return y