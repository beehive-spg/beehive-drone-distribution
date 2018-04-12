#!/usr/bin/env python3
import collections
import json
from distribution.foundation.logger import Logger
from distribution.rabbitmq import publisher
from distribution.service import hiveservice, buildingservice, locationservice

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
        new_ratio = get_io_ratio(hive.incoming+hive.free, hive.outgoing)
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
    neighbor_ranking = get_neighbor_ranking(hive)
    neighbor_ranking_items = list(neighbor_ranking.items())
    _from = list(neighbor_ranking.keys())[0]
    building = buildingservice.get_building_by(hive.id)
    send(_from, building.id)

def get_neighbor_ranking(hive):
    building = buildingservice.get_building_by(hive.id)
    cost_ranking = dict()
    buildingdomains = dict()
    neighbors = hiveservice.get_reachable_hives(hive.id)
    for neighbor in neighbors:
        neighbor_building = buildingservice.get_building_by(neighbor.id)
        distribution_cost = hiveservice.get_hivecost(neighbor_building.id)
        cost_ranking[neighbor_building.id] = distribution_cost
        buildingdomains[neighbor_building.id] = neighbor_building
    ordered_ranking = get_ordered_ranking(cost_ranking)

    logger.info("-------hivecost ranking-------")
    logger.info(ordered_ranking)

    distance_ranking = dict()
    hivecost = 4
    while(len(distance_ranking) <= 0):
        for key, value in ordered_ranking.items():
            if(value < hivecost):
                distance_ranking[key] = locationservice.get_distance((buildingdomains[key].xcoord, buildingdomains[key].ycoord), (building.xcoord, building.ycoord))
        hivecost += 0.5

    logger.info("-------distance ranking-------")
    logger.info(get_ordered_ranking(distance_ranking))

    return get_ordered_ranking(distance_ranking)

def get_ordered_ranking(ranking):
    return collections.OrderedDict(sorted(ranking.items(), key=lambda t: t[1]))

def send(_from, to):
    distribution = dict()
    distribution['from'] = str(_from)
    distribution['to'] = str(to)
    publisher.send_distribution(json.dumps(distribution))