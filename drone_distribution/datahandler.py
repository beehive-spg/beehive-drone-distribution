#!/usr/bin/env python3
import drone_distribution.test_requests as tr
from drone_distribution import rest
import json, datetime, base64, sys

def get_workload_in(time, _id):
	orders = get_orders_in(time, _id)
	drones = get_drones_in(time, _id)
	return orders / drones

def get_amount_of_drones_for(_id):
	workload = get_workload_in(0, _id)
	orders = get_orders_in(get_time_of_impact(), _id)
	drones = get_drones_in(get_time_of_impact(), _id)
	return drones - (orders / workload)

# TODO: get remaining charging time
def get_time_of_impact():
	types = rest.get_types()
	flying_time = get_flying_time(types)
	chargetime = get_chargetime_of_drone(types)
	return flying_time + charging_time

def get_flying_time():
	speed = get_speed_of_drone()
	distance = get_distance_between(10,10)
	return distance / speed

def get_speed_of_drone(types):
	return types['speed']

def get_range_of_drone(types):
	return types['range']

def get_chargetime_of_drone(types):
	return types['chargetime']

# rising or decreasing
def get_prediction_status(_id):
	current_workload = get_workload_in(0, _id)
	predicted_workload = get_workload_in(get_time_of_impact(), _id)
	return predicted_workload - current_workload

def get_sum_of_workload_of(_id):
	current_workload = get_workload_in(0, _id)
	_sum = current_workload
	predicted_workload_inbetween = get_workload_in(get_time_of_impact()/2, _id)
	_sum += predicted_workload_inbetween
	predicted_workload_at_drone_arrival = get_workload_in(get_time_of_impact(), _id)
	_sum += predicted_workload_at_drone_arrival
	return _sum

# TODO: adapt to database
def get_drones_in(time, _id):
	drones = rest.get_drones_in(time, _id)
	return drones['drones']

# TODO: adapt to database
def get_orders_in(time, _id):
	return rest.get_orders_in(time, _id)

# eotd true, returns drones needed for the next day
# eotd false, returns drones needed to harm the network as little as possible
def get_drones_to_send(_id, eotd):
	if (eotd):
		return get_needed_drones(_id)
	return get_drones_without_impact(_id)

# TODO: adapt to database
# TODO: non existing id? possible?
def get_free_drones(_id, hives):
	for hive in hives:
		if (hive['id'] == _id):
			return hive['free']
	return -1

def get_reachable_hives(_id):
	reachable_hives = rest.get_reachable_hives(_id)
	reachable = []
	for hive in reachable_hives:
		if (hive['start']['id'] == _id):
			reachable.append(hive['id'])
		elif (hive['end']['id'] == _id):
			reachable.append(hive['id'])
	return reachable

def get_hive_drone_status_now(_id):
	return get_hive_drone_status(_id, datetime.datetime.now())

# returns if a hive needs drones or can give drones
# true can give, false cannot
def get_hive_drone_status(_id, time):
	number_of_drones = get_needed_drones(_id, time)
	if (number_of_drones > 0):
		return True
	return False

def get_url_safe_date_for_the_next_day():
	date = get_date_for_the_next_day()
	encoded = base64.urlsafe_b64encode("%d" % int(date))
	return encoded

def get_date_for_the_next_day():
	now = datetime.datetime.now()
	if (now.hour < 6):
		date = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)
	else:
		date = datetime.datetime(now.year, now.month, now.day+1, 9, 0, 0)
	return date

# returns number of drones needed(+) or missing(-)
def get_needed_drones(_id, time):
	demand = get_drone_demand(time, _id)
	supply = get_drone_supply(time, _id)
	return demand - supply

def get_map_border():
	upper_y = upper_x = -1
	lower_y = lower_x = sys.maxsize
	for key, value in get_hive_locations().items():
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
	for key, value in get_hive_locations().items():
		y_values.append(value.y)
	y_values.sort(reverse=descending)
	return y_values

def get_x(descending=False):
	x_values = []
	for key, value in get_hive_locations().items():
		x_values.append(value.x)
	x_values.sort(reverse=descending)
	return x_values

def get_hives_by_x(x):
	hives = []
	hive_locations = get_hive_locations()
	for hive in hive_locations:
		if (hive_locations[hive].x == x):
			hives.append(hive)
	return hives

def get_hives_by_y(y):
	hives = []
	hive_locations = get_hive_locations()
	for hive in hive_locations:
		if (hive_locations[hive].y == y):
			hives.append(hive)
	return hives

# returns dict with ids and coordinates
def get_hive_locations():
	all_hives = rest.get_all_hives()
	hives = dict()
	for hive in all_hives:
		hives[hive['id']] = Point(hive['xcoord'], hive['ycoord'])
	return hives;

def get_hives_with_drones():
	hives_with_drones = get_hives_with_drones()
	hives = dict()
	for hive in hives_with_drones:
		hives[hive['id']] = hive['drones']
	return hives;

#for testing purposes
def set_drones_for_hive(hiveid, amount):
	#drones = []
	for nr in range(amount):
		drone = dict()
		drone['hiveid'] = hiveid
		drone['name'] = "drone-"+str(nr)
		drone['status'] = ":status/IDLE"
		#drones.append(drone)
		rest.post_hive_drone(json.dumps(drone, ensure_ascii=False))


### ---------------------------------------- OPTIONAL
def get_upper_y_from(hive_locations):
	y = 0
	for key, value in hive_locations.items():
		if (y < value.y):
			y = value.y
	return y

def get_upper_x_from(hive_locations):
	x = 0
	for key, value in hive_locations.items():
		if (x < value.x):
			x = value.x
	return x

def get_lower_y_from(hive_locations):
	y = 0
	for key, value in hive_locations.items():
		if (y > value.y):
			y = value.y
	return y

def get_lower_x_from(hive_locations):
	x = 0
	for key, value in hive_locations.items():
		if (x > value.x):
			x = value.x
	return x

def get_average_workload():
	return rest.get_average_workload()

def get_impact_to(_id, drones):
	future_orders = get_orders_in(get_time_of_impact(), _id)
	future_drones = get_drones_in(get_time_of_impact(), _id)
	future_drones += drones
	return future_orders / future_drones

def get_hive_weight_evaluation():
	#weight_evaluation = database connection
	return weight_evaluation

def get_number_of_hives():
	return len(get_all_hives())

'''
def get_drone_demand(time, _id):
	return tr.request_drone_demand(time, _id)

def get_drone_supply():
	return tr.request_drones_in(time_id)
'''