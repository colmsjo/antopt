# pylint: disable=missing-docstring, global-statement
#
# ANT[antno] = (current_node, accumulated_dist, [visited_nodes])
#
# Each cycle has number of node - 1 steps
#
# These constants give best results according to Dorigo (1996)
#
# ALPHA = 1
# BETA = 5
# RHO = 0.5
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)


# Imports
# =======

from random import random
import sys
import copy
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


# Data structures
# ===============

C = 0.1                 # Initial pheromone on each edge
Q = 1.0                 # Pheromone deposit
T = 0                   # time counter
RHO = 0.5               # Evaporation
NCMAX = 100             # maximum number of cycles
PHEROMONE_MAP = None

ANT = None
START_NODE = None
NO_OF_ANTS = 10

ALPHA = 1
BETA = 5

def init(filename):
    global ANT, C, PHEROMONE_MAP, START_NODE, RHO

    # Open the map file and calculate the distances
    map_funcs.open_map(filename)
    map_funcs.calc_distances()

    # Create a pheromone map by copying the edges
    PHEROMONE_MAP = copy.deepcopy(map_funcs.EDGES)

    # Initialize edges with pheromones ()
    for m in map_funcs.EDGES:

        if START_NODE is None:
            START_NODE = m

        for n in map_funcs.EDGES[m]:
            if PHEROMONE_MAP[n][m] == C:
                PHEROMONE_MAP[m][n] = None
            else:
                PHEROMONE_MAP[m][n] = C

    # Initialize the ants
    ANT = [(START_NODE, 0, x[:]) for x in [[]] * NO_OF_ANTS]


# Pheromone functions
# ===================

def get_pheromone(node1, node2):
    if PHEROMONE_MAP[node1][node2] is not None:
        return PHEROMONE_MAP[node1][node2]

    if PHEROMONE_MAP[node2][node1] is not None:
        return PHEROMONE_MAP[node2][node1]

    error('get_pheromone: edge {:s} {:s} does not exist'.format(node1, node2))
    return None

def deposit_pheromone(node1, node2, amount):
    if PHEROMONE_MAP[node1][node2] is not None:
        PHEROMONE_MAP[node1][node2] += amount
    elif PHEROMONE_MAP[node2][node1] is not None:
        PHEROMONE_MAP[node2][node1] += amount
    else:
        error('deposit_pheromone: edge {:s} {:s} does not exist'.format(node1, node2))
        return None

def deposition_pheromone_it(antno):
    (current_node, accumulated_dist, visited_nodes) = ANT[antno]

    nodes = copy.copy(visited_nodes)
    while nodes:
        prev_node = nodes.pop()
        deposit_pheromone(current_node, prev_node, Q/accumulated_dist)
        current_node = prev_node

def evaporate_pheromone():
    for node1 in PHEROMONE_MAP:
        for node2 in PHEROMONE_MAP[node1]:
            if PHEROMONE_MAP[node1][node2] is not None:
                 PHEROMONE_MAP[node1][node2] *= (1-RHO)

# Manage ants
# ===========

def calc_transition_probabilities(antno):

    denom = 0
    (current_node, _, visited_nodes) = ANT[antno]
    for node in map_funcs.EDGES[current_node]:
        if node not in visited_nodes:

            denom += (pow(get_pheromone(current_node, node), ALPHA) *
                      pow(1/map_funcs.EDGES[current_node][node], BETA))

    transition_probabilities = []
    for node in map_funcs.EDGES[current_node]:
        if node not in visited_nodes:
            transition_probabilities += [(current_node, node,
                                          (pow(get_pheromone(current_node, node), ALPHA) *
                                           pow(1/map_funcs.EDGES[current_node][node], BETA))/denom,
                                          map_funcs.EDGES[current_node][node])]

    return transition_probabilities

def select_random_edge(transition_probabilities):
    transition_probabilities.sort(key=lambda x: 1-x[2])

    # 0 < r < 1 (avoid that r is 0)
    r = 0
    while r == 0:
        r = random()

    prob_sum = 0.0
    i = 0
    while prob_sum < r:
        node1, node2, prob, dist = transition_probabilities[i]
        prob_sum += prob
        i += 1

    return (node1, node2, dist)

def move(antno):
    (current_node, accumulated_dist, visited_nodes) = ANT[antno]

    (node1, node2, dist) = select_random_edge(calc_transition_probabilities(antno))
    assert current_node == node1 or current_node == node2

    visited_nodes += current_node
    accumulated_dist += dist

    if current_node != node1:
        current_node = node1
    else:
        current_node = node2

    ANT[antno] = (current_node, accumulated_dist, visited_nodes)

def all_nodes_visited(antno):
    (_, _, visited_nodes) = ANT[antno]
    return len(visited_nodes) == len(map_funcs.NODES) - 1

def empty_dist_and_visited():
    for antno in range(0, len(ANT)):
        (_, _, _) = ANT[antno]
        ANT[antno] = (START_NODE, 0, [])

def sort_ants():
    ANT.sort(key=lambda x: x[1])

# Check if all ants have taken the same route
def stagnation():
    # Make sure visited_nodes aren't empty
    if not ANT[0][2]:
        return False

    res = True
    i = 1
    while res and i < len(ANT):
        res = ANT[i-1][2] == ANT[i][2]
        i += 1

    return res

# Main
# ====

def run():
    init(sys.argv[1])
    cycleno = 0
    best_ant = (None, float('inf'), [])

    while not stagnation() and cycleno < NCMAX:
        empty_dist_and_visited()
        for antno in range(0, NO_OF_ANTS):
            for moveno in range(0, len(map_funcs.EDGES)):
                if not all_nodes_visited(antno):
                    move(antno)

            deposition_pheromone_it(antno)

        if DEBUG_MODE:
            sys.stdin.read(1)
            print("cycleno:{:d}, moveno:{:d}, antno: {:d}".format(cycleno,
                                                                moveno,
                                                                antno), ANT, PHEROMONE_MAP)

        evaporate_pheromone()
        sort_ants()

        if ANT[0][1] < best_ant[1]:
            best_ant = ANT[0]

        print("Cycle: {:d}".format(cycleno), ANT[0], ANT[len(ANT)-1])

        cycleno += 1

    print('Best ant:', best_ant)
    print('Total number of nodes: {:d}'.format(len(best_ant[2])+1))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python ants.py <MAP>', sys.argv)
        exit(0)

    run()
