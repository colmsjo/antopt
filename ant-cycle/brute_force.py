# pylint: disable=missing-docstring, global-statement
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)


# Imports
# =======

import sys
import math
import numpy
import map_funcs


# Setup logging
# =============

DEBUG_MODE = False

def debug(*args):
    print('DEBUG:ants:', *args)

def error(*args):
    print('ERROR:ants:', *args)

def warn(*args):
    print('WARNING:ants:', *args)


# Calc all routes
# ===============


def all_routes(nodes):
    if len(nodes) <= 1:
        return [[]]

    res = []
    head = nodes.pop(0)
    for i in range(0, len(nodes)):
        nodes_cp = nodes[:]
        next_node = nodes_cp.pop(i)
        res += [[(head, next_node)] + x for x in all_routes([next_node]+nodes_cp)]

    return res

def calc_dist(route):
    res = 0
    for (node1, node2) in route:
        res += map_funcs.EDGES[node1][node2]

    return res


# Main
# ====

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python map_funcs.py <MAP>', sys.argv)
        exit(0)

    map_funcs.open_map(sys.argv[1])
    map_funcs.calc_distances()

    res = all_routes(list(map_funcs.NODES.keys()))
    print('Number of nodes: {:d}, Number of routes: {:d}, Expected number of routes: {:d}'.format(
        len(map_funcs.NODES), len(res),  math.factorial(len(map_funcs.NODES)-1)))

    distances = list(map(calc_dist, res))
    print('Min distance: {:.2f}, Max distance: {:.2f}'.format(
        min(distances), max(distances)))

    min_route = res[numpy.argmin(distances)]
    max_route = res[numpy.argmax(distances)]
    min_route_nodes = list(map(lambda x: x[0], min_route))+[min_route[-1][1]]
    max_routes_nodes = list(map(lambda x: x[0], max_route))+[max_route[-1][1]]
    print('Route with min distance:', min_route_nodes)
    print('Route with max distance:', max_routes_nodes)
