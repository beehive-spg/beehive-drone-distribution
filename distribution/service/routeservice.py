#!/usr/bin/env python3
from distribution.domain.route import Route
from distribution.rest import rest
from distribution.foundation.exceptions import domain_id_error

def get_all_routes():
    all_routes = rest.get_all_routes()
    routes = []
    for route in all_routes:
        routedomain = get_routedomain(route)
        routes.append(routedomain)
    return routes

def get_routedomain(json):
    route = Route(json)
    route.validate()
    return route

def get_route_by(routeid):
    all_routes = get_all_routes()
    for route in all_routes:
        if (route.id == routeid):
            return route
    raise domain_id_error("Route", routeid)

def get_hop_in_route(route, hopid):
    for hop in route.hops:
        if (hop.id == hopid):
            return hop

def get_total_distance(route):
    distance = 0
    for hop in route.hops:
        distance += hop.distance
    return distance

def get_distance_until_hop(route, current_hop):
    distance = 0
    for hop in route.hops:
        if (hop.id != current_hop.id):
            distance += hop.distance
    return distance

def get_route_distance_progress(route, current_hop):
    distance_for_next_hop = current_hop.distance
    total_distance = get_total_distance(route)
    return distance_for_next_hop / total_distance