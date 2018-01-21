import requests as r

port = 3000
url = "localhost:"

def get_orders_in(time, _id):
	orders = r.get(url("/hives/workload/:"+time+"/:"_id))
	return orders.json()

def get_drones_in(time, _id):
	drones = r.get(url("/"))
	return drones.json()

def get_neighborhood_hives(_id):
	neighbors = r.get(url("/"))
	return [11,22,33,44]

def get_flying_time():
	flying_time = r.get(url("/"))
	return flying_time.json()

def get_charging_time():
	charging_time = r.get(url("/"))
	return charging_time.json()

def get_available_drones(_id):
	drones = r.get(url("/"))
	return drones.json()

def get_average_workload():
	workload = r.get(url("/"))
	return workload.json()

def get_hive_weight_evaluation():
	evaluation = r.get(url("/"))
	return evaluation.json()

def get_number_of_moved_drones():
	drones = r.get(url("/"))
	return drones.json()

def get_all_hives():
	hives = r.get(url("/hives"))
	return hives.json()

def put_hive_weight(_id, weight):
	data = dict()
	data[_id] = weight
	r.put(url("/"), str(data)

def put_hive_weights(weights):
	r.put(url("/"), str(weights))

def url(route):
	return url + port + route