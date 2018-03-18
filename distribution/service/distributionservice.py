#!/usr/bin/env python3
from distribution.foundation.logger import Logger
from distribution.rabbitmq import publisher
from distribution.service import hiveservice, buildingservice, locationservice
import collections

logger = Logger(__name__)

def get_complete_hivedomain(hive):
    incoming = hiveservice.get_number_of_incoming_hops(hive.id)
    outgoing = hiveservice.get_number_of_outgoing_hops(hive.id)
    free = hiveservice.get_free_drones(hive)
    hive.incoming = incoming
    hive.outgoing = outgoing
    hive.free = free
    return hive

def get_complete_buildingdomain(building):
    building.hive = get_complete_hivedomain(building.hive)
    return building

def get_io_ratio_of_hive(hive):
    incoming = hiveservice.get_number_of_incoming_hops(hive.id)
    outgoing = hiveservice.get_number_of_outgoing_hops(hive.id)
    io_ratio = get_io_ratio(incoming, outgoing)
    if (io_ratio == 0):
        if(incoming > 0):
            io_ratio = get_io_ratio(incoming, 1)
        else:
            io_ratio = get_io_ratio(incoming+hive.free, outgoing)
    return io_ratio

def get_io_ratio(incoming, outgoing):
    if (incoming != 0 and outgoing != 0):
        return incoming / outgoing
    return 0

def is_needing_drone(io_ratio, hive):
    if (io_ratio < 1):
        new_ratio = get_io_ratio(incoming+hive.free, outgoing)
        if (new_ratio < 1):
            return True
    return False

def evaluate_hive(hive):
    hive.free = hiveservice.get_free_drones(hive)
    io_ratio = get_io_ratio_of_hive(hive)
    if (io_ratio != 0):
        if (is_needing_drone(io_ratio, hive)):
            distribute_to(hive)
        else:
            logger.info("distribution to hive {} is not needed - io: {}"
                        .format(hive.id, io_ratio))
    else:
        outgoing = hiveservice.get_number_of_outgoing_hops(hive.id)
        if (outgoing > hive.free):
            distribute_to(hive)

def distribute_to(hive):
    logger.info("distribution from {} has started".format(hive.id))
    neighbor_ranking = list(get_neighbor_ranking(hive).items())
    _from = neighbor_ranking[0]
    for rank in neighbor_ranking:
        logger.info("rankings {}".format(rank))
    logger.info("distribution from {} starting".format(_from))

def get_neighbor_ranking(hive):
    building = buildingservice.get_building_by(hive.id)
    ranking = dict()
    neighbors = hiveservice.get_reachable_hives(hive.id)
    for neighbor in neighbors:
        neighbor_building = buildingservice.get_building_by(neighbor.id)
        distribution_cost = get_distribution_cost(building, neighbor_building)
        ranking[neighbor_building.id] = distribution_cost
    return get_ordered_ranking(ranking)

def get_distribution_cost(building, neighbor):
    distance_cost = get_distance_cost(building, neighbor)
    workload_cost = get_workload_cost(neighbor)
    return distance_cost * workload_cost - neighbor.hive.free

def get_distance_cost(building, neighbor):
    building_location = (building.xcoord, building.ycoord)
    neighbor_location = (neighbor.xcoord, neighbor.ycoord)
    return locationservice.get_distance(building_location, (neighbor_location))

def get_workload_cost(neighbor):
    neighbor = get_complete_buildingdomain(neighbor)
    io_ratio = get_io_ratio_of_hive(neighbor.hive)
    neighbor.hive.outgoing += 1
    new_io_ratio = get_io_ratio_of_hive(neighbor.hive)
    difference = new_io_ratio - io_ratio
    return difference

def get_ordered_ranking(ranking):
    return collections.OrderedDict(sorted(ranking.items(), key=lambda t: t[1]))

def send(_from, to):
    distribution = dict()
    distribution['from'] = str(_from)
    distribution['to'] = str(to)
    publisher.send_distribution(distribution)
    logger.info("sending from: {} - to: {}".format(_from, to))