# Ant Colony Optimization used to solve the travelling salesman problem

"""
Cities are represented as nodes where each node has a list of legs to other cities
Legs are tuples containing a cost and pheromone (deposited by the ants)

city[i] = [(legno1, cityj), ..., (legno,cityj)]
leg[i] = (cost, pheromone)

          0           Costs for the legs:
     0 ------- 1
     |\ 1    / |      0 - 10
     |  \  /5  |      1 - 7
  2  |    x    | 3    2 - 20
     |  /   \  |      3 - 2
     |/       \|      4 - 2
     2 ------- 3      5 - 5
          4

"""

from random import random
import sys

# Setup logging
# =============

DEBUG_MODE = False

def debug(*args):
    print('DEBUG:ants:', *args)

def error(*args):
    print('ERROR:ants:', *args)

def warn(*args):
    print('WARNING:ants:', *args)

#
# Setup data structure
# ====================

DEBUG_MODE = False

# Some constants
NO_OF_ANTS = 10
PHEROMONE_DEPOSIT = 1
START_PHEROMONE = 0.1
NO_OF_GENERATIONS = 5
NO_MOVES_PER_ANT = 10
START_NODE = 0
STOP_NODE = 2
EVAPORATION = 0.1

# Create array with 4 nodes representing the cities. Each city has a list of tuples with legno and the city it leads to
# node[(legno, cityno)]
node = [None] * 4

node[0] = [(0,1), (1,3), (2,2)]
node[1] = [(0,0), (3,3), (5,2)]
node[2] = [(2,0), (5,1), (4,3)]
node[3] = [(4,2), (1,0), (3,1)]


# Create array with 6 legs
# leg(cost, pheromone) - using 1 as initial pheromone to aviod divide by zero
leg = [None] * 6

def init_leg():
  global leg
  leg[0] = (10,START_PHEROMONE)
  leg[1] = (7,START_PHEROMONE)
  leg[2] = (20,START_PHEROMONE)
  leg[3] = (2,START_PHEROMONE)
  leg[4] = (2,START_PHEROMONE)
  leg[5] = (5,START_PHEROMONE)


# Create the ants, all in node 0 with a total accumulated cost of 0
# ant[i] = (current_node, accumulated_cost)
ant = None
def init_ant():
  global ant
  ant = [(START_NODE, x[:]) for x in [[]] * NO_OF_ANTS]


#
# ant functions
# =============

def deposit_pheromone(legno):
  (cost, current_pheromone) = leg[legno]
  leg[legno] = (cost, current_pheromone + PHEROMONE_DEPOSIT / cost)

def evaporate_pheromone():
  for legno in range(0, len(leg)):
    (cost, pheromone) = leg[legno]
    pheromone *= (1-EVAPORATION)
    leg[legno] = (cost, pheromone)

def calc_transition_probabilities(antno):
  (current_node, visited_nodes) = ant[antno]
  total_pheromone = 0
  for legno, to_city in node[current_node]:
    (cost, pheromone) = leg[legno]
    total_pheromone += pheromone

  transition_probabilities = []
  for legno, to_city in node[current_node]:
    (cost, pheromone) = leg[legno]
    transition_probabilities += [(legno, pheromone/total_pheromone)]

  return transition_probabilities


def select_random_leg(transition_probabilities):
  transition_probabilities.sort(key=lambda x: 1-x[1])

  # 0 < r < 1 (avoid that r is 0)
  r = 0
  while r == 0:
    r = random()

  prob_sum = 0.0
  i = 0
  while prob_sum < r:
    legno, prob = transition_probabilities[i]
    prob_sum += prob
    i += 1
  return legno


def move(antno):
  if ant[antno][0] is None:
    return

  (current_node, visited_nodes) = ant[antno]

  probs = calc_transition_probabilities(antno)

  selected_legno = select_random_leg(probs)
  selected_node = list(filter(lambda x: x[0] == selected_legno, node[current_node]))[0][1]

#  if antno == 0:
#    debug('move: probs: ', probs, 'current node: ', current_node, 'selected leg: ', selected_legno, 'selected node: ', selected_node, 'legs: ', leg)

  deposit_pheromone(selected_legno)

  visited_nodes += [selected_node]
  if selected_node == STOP_NODE:
    ant[antno] = (None, visited_nodes)
  else:
    ant[antno] = (selected_node, visited_nodes)

#
# Output functions
# ================

def format_list(l):
  res = ""
  for i,e in enumerate(l):
    if i != 0:
      res += ", "
    res += str(i) + ":" + str(e)
  return res

def format_cost():
  return """
              10
         0 ------- 1
         |\ 7    / |
         |  \  /5  |
      20 |    x    | 2
         |  /   \  |
         |/       \|
         2 ------- 3
              2
    """

def format_legs(l):
  """ Leg numbers:
            0
       0 ------- 1
       |\ 1    / |
       |  \  /5  |
    2  |    x    | 3
       |  /   \  |
       |/       \|
       2 ------- 3
            4
  """
  s  = "\n           {:.1f}\n".format(leg[0][1])
  s += "       0 ------- 1\n"
  s += "       |\ {:.1f}  / |\n".format(leg[1][1])
  s += "       |  \  /{:.1f}|\n".format(leg[5][1])
  s += "   {:.1f} |    x    | {:.1f}\n".format(leg[2][1], leg[3][1])
  s += "       |  /   \  |\n"
  s += "       |/       \|\n"
  s += "       2 ------- 3\n"
  s += "          {:.1f}".format(leg[4][1])

  return s


#
# Main
# ====

def stagnation():
  return len(list(filter(lambda x: x[0] is not None, ant))) == 0

def run():
  for genno in range(0, NO_OF_GENERATIONS):
    init_leg()
    init_ant()
    if DEBUG_MODE:
      sys.stdin.read(1)
      print("genno:{:d}, moveno:{:d}, antno: {:d}".format(genno, moveno, antno), " - legs:", format_list(leg))

    moveno = 0
    while moveno < NO_MOVES_PER_ANT and not stagnation():
      for antno in range(0, NO_OF_ANTS):
        move(antno)
      evaporate_pheromone()
      moveno += 1

    print("\n\nGeneration: {:d}".format(genno))
    print('legs: ', format_legs(leg))
    print('ants: ', ant)


if __name__ == '__main__':
  print("\n\nCosts:", format_cost())
  run()
  print("nodes:", format_list(node))
  print("legs:", format_list(leg))
