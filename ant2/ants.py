# pylint: disable=missing-docstring, global-statement
#
# * ANT[antno] = ((x, y), (dx, dy))
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)


# Imports
# =======

from random import random
import sys
import map_funcs


# Setup logging
# =============

def debug(*args):
    print('DEBUG:ants:', *args)

def error(*args):
    print('ERROR:ants: ', *args)

def warn(*args):
    print('WARNING:ants: ', *args)


# Ant funtions
# ============

NO_OF_ANTS = 10
NO_OF_GENERATIONS = 5
NO_MOVES_PER_ANT = 20

ANT = [((None, None), (None, None))] * NO_OF_ANTS

# All ants starts in the first node
def init():
    (_, x, y) = map_funcs.get_nodes()[0]
    for antno in range(0, NO_OF_ANTS):
        ANT[antno] = ((x, y), (None, None))

def format_ants():
    return ','.join(str(a) for a in ANT)

def get_ant(antno):
    return ANT[antno]

def move(antno):
    ((x, y), (dx, dy)) = ANT[antno]

    if map_funcs.is_node(x, y):
        (dx, dy) = select_random_leg(calc_transition_probabilities(x, y,
                                                                   dx, dy))

    x += dx
    y += dy

    if map_funcs.is_leg(x, y):
        map_funcs.deposit_pheromone(x, y)

    ANT[antno] = ((x, y), (dx, dy))

def calc_transition_probabilities(x, y, dx, dy):
    (dx1, dy1) = (dx, dy)
    legs_for_node = map_funcs.get_legs(None, x, y)

    if dx1 != None and dy1 != None:
        legs_for_node = list(filter(lambda t: t[1] != (-1*dx1, -1*dy1),
                                legs_for_node))

    total_pheromone = 0
    for (legno, (dx1, dy1), cost, pheromone) in legs_for_node:
        total_pheromone += pheromone

    transition_probabilities = []
    for (legno, (dx1, dy1), cost, pheromone) in legs_for_node:
        transition_probabilities += [(legno, pheromone/total_pheromone,
                                      (dx1, dy1))]

    return transition_probabilities

def select_random_leg(transition_probabilities):
    transition_probabilities.sort(key=lambda x: 1-x[1])

    # 0 < r < 1 (avoid that r is 0)
    r = 0
    while r == 0:
        r = random()

    dxdy = None
    prob_sum = 0.0
    i = 0
    while prob_sum < r:
        legno, prob, dxdy = transition_probabilities[i]
        prob_sum += prob
        i += 1

    return dxdy

# Main
# ====

def run():
    for genno in range(0, NO_OF_GENERATIONS):
        for moveno in range(0, NO_MOVES_PER_ANT):
            for antno in range(0, NO_OF_ANTS):
                move(antno)

            map_funcs.evaporate()
        print('\nGeneration {:d}\n'.format(genno),
              map_funcs.format_pheromone_map())

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python ants.py <MAP>', sys.argv)
        exit(0)

    map_funcs.open_map(sys.argv[1])
    init()
    run()
