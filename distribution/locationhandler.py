import sys
from drone_distribution import datahandler, rest

def get_average_distance_to(_id):
	reachable_buildings = rest.get_reachable_buildings()
	distance = []
	for hive in reachable_buildings:
		if (hive['end']['id'] == _id or hive['start']['id'] == _id):
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

def get_map_border():
	upper_y = upper_x = -1
	lower_y = lower_x = sys.maxsize
	for key, value in datahandler.get_hive_locations().items():
		if (upper_y < value.y):
			upper_y = value.y
		if (value.y < lower_y):
			lower_y = value.y
		if (upper_x < value.x):
			upper_x = value.x
		if (value.x < lower_x):
			lower_x = value.x
	return [ upper_y, upper_x, lower_y, lower_x ]

def get_y(descending=False):
	y_values = []
	for key, value in datahandler.get_hive_locations().items():
		y_values.append(value.y)
	y_values.sort(reverse=descending)
	return y_values

def get_x(descending=False):
	x_values = []
	for key, value in datahandler.get_hive_locations().items():
		x_values.append(value.x)
	x_values.sort(reverse=descending)
	return x_values

def get_hives_by_x(x):
	hives = []
	hive_locations = datahandler.get_hive_locations()
	for hive in hive_locations:
		if (hive_locations[hive].x == x):
			hives.append(hive)
	return hives

def get_hives_by_y(y):
	hives = []
	hive_locations = datahandler.get_hive_locations()
	for hive in hive_locations:
		if (hive_locations[hive].y == y):
			hives.append(hive)
	return hives

def get_upper_x(hive_locations):
	x = -1
	for key, value in hive_locations.items():
		if (x < value.x):
			x = value.x
	return x

def get_upper_y(hive_locations):
	y = -1
	for key, value in hive_locations.items():
		if (y < value.y):
			y = value.y
	return y

def get_lower_x(hive_locations):
	x = sys.maxsize
	for key, value in hive_locations.items():
		if (x > value.x):
			x = value.x
	return x

def get_lower_y(hive_locations):
	y = sys.maxsize
	for key, value in hive_locations.items():
		if (y > value.y):
			y = value.y
	return y