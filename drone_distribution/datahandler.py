#!/usr/bin/env python3
from drone_distribution import test_requests as tr

def get_workload_in(time, _id):
	orders = get_orders_in(time, _id)
	drones = get_drones_in(time, _id)
	return orders / drones

def get_amount_of_drones_for(_id):
	workload = get_workload_in(0, _id)
	orders = get_orders_in(get_time_of_impact(), _id)
	drones = get_drones_in(get_time_of_impact(), _id)
	return drones - (orders / workload)

# get average time to fly + charge
# maybe query for all avg or only regarding distance to surrounded hives
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

def get_average_workload():
	return tr.request_average_workload()

# request returns probably json, except I implement otherwise
# might request only a certain amount of hives
# --> nearest 10 (number of needed drones)
def get_neighborhood_from(_id):
	return tr.request_neighborhood_hives(_id) # list of _ids


# returns the workload raise of a hive
# number of drones decreases for every point in time (in 20, 30, 50 minutes)
# each workload goes up
def get_impact_to(_id, drones):
	orders = get_orders_in(get_time_of_impact(), _id)
	drones = get_drones_in(get_time_of_impact(), _id)
	drones += drones
	return orders / drones

def get_hive_weight_evaluation():
	#weight_evaluation = database connection
	return weight_evaluation

# returns if a hive needs drones or can give drones
# true needs, false can give
def get_hive_drone_status(_id):
	number_of_drones = get_needed_drones(_id)
	if (number_of_drones > 0):
		return true
	return false

# returns number of drones needed(+) or missing(-)
def get_needed_drones(_id):
	demand = tr.request_drone_demand(_id)
	supply = tr.request_drones_in(0, _id)
	return demand - supplys

def get_all_hives():
	return tr.reqeust_all_hives()

def get_hive_id_by(message):
	parsed_message = json.loads(message)
	return parsed_message['id']