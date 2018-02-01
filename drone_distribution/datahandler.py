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

def get_time_of_impact():
	flying_time = tr.request_flying_time()
	charging_time = tr.request_charging_time()
	return flying_time + charging_time

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

def get_drones_in(time, _id):
	return tr.request_drones_in(time, _id)

def get_orders_in(time, _id):
	return tr.request_orders_in(time, _id)

# eotd true, returns drones needed for the next day
# eotd false, returns drones needed to harm the network as little as possible
def get_drones_to_send(_id, eotd):
	if (eotd):
		return get_needed_drones(_id)
	return get_drones_without_impact(_id)

def get_drones_without_impact(_id):
	return tr.request_available_drones(_id)

def get_neighborhood_from(_id):
	return tr.request_neighborhood_hives(_id) # list of _ids

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

def get_drone_demand(time, _id):
	return tr.request_drone_demand(time, _id)

def get_drone_supply():
	return tr.request_drones_in(time_id)

def get_all_hives():
	return tr.reqeust_all_hives()

def get_hive_id_by(message):
	parsed_message = json.loads(message)
	return parsed_message['id']

def get_hive_location_by(message):
	parsed_message = json.loads(message)
	return parsed_message['location']

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
	tr_hives = get_all_hives()
	hives = dict()
	for hive in tr_hives:
		hives['id'] = Point(hive['lon'], hive['lat'])
	return hives;

def get_hives_with_drones():
	tr_hives = get_hives_with_drones()
	hives = dict()
	for hive in tr_hives:
		hives['id'] = hive['drones']
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
	return tr.request_average_workload()

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