# pylint: disable=missing-docstring, global-statement, misplaced-comparison-constant; good-names=x,y
#
# * get_node_ids(): ['a', ..., 'z']
# * legs_for_node[nodeid] = [(legno, (dx, dy), cost, pheromone)]
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)

# Module variables
# ===============

MAP = None
PHEROMONE_MAP = None
NODE = None
PHEROMONE = 1
EVAPORATION = 0.9
NUMBER_OF_LEGS = 0
LEGS_FOR_NODE = {}
AXIS = {'X': (1, 0), 'Y': (0, 1), 'Z': (1, 1), 'W': (-1, 1)}


# Setup logging
# =============

def debug(*args):
    print('DEBUG:map_funcs:', *args)

def error(*args):
    print('ERROR:map_funcs:', *args)

def warn(*args):
    print('WARNING:map_funcs:', *args)


# Map functions
# =============

def open_map(filename):
    global MAP, PHEROMONE_MAP
    filehandle = open(filename)
    m = filehandle.read().strip().split('\n')
    NODES = m[0]
    MAP = m[1:]
    PHEROMONE_MAP = [x[:] for x in [[1.0] * len(MAP[0])] * len(MAP)]
    filehandle.close()

def format_map():
    return '\n'.join(str(l) for l in MAP)

def format_pheromone_map():
    res = ''
    for row in range(0, len(PHEROMONE_MAP)):
        for col in range(0, len(PHEROMONE_MAP[row])):
            if is_leg(col, row):
                res += '{:.2f} '.format(PHEROMONE_MAP[row][col])
            elif is_node(col, row):
                res += ' ' + MAP[row][col] + '   '
            else:
                res += '     '
        res += '\n'
    return res

def is_node(col, row):
    return (row >= 0 and col >= 0 and row < len(MAP) and col < len(MAP[row])
            and ord('a') <= ord(MAP[row][col])
            and ord(MAP[row][col]) <= ord('z'))

def is_leg(col, row):
    return (row >= 0 and col >= 0 and row < len(MAP) and col < len(MAP[row])
            and ord('A') <= ord(MAP[row][col])
            and ord(MAP[row][col]) <= ord('Z'))

def get_leg_cost(col, row):
    return ord(MAP[row][col]) - ord('X') + 1

def iterate_over_map(fnc):
    for lineno in range(0, len(MAP)):
        for colno in range(0, len(MAP[lineno])):
            fnc(MAP[lineno][colno], colno, lineno)

def get_nodes():
    nodes = []
    iterate_over_map((lambda c, col, row: nodes.append((c, col, row))
                      if is_node(col, row) else None))
    return nodes

def find_node(nodeid):
    res = []
    iterate_over_map((lambda c, col, row: res.append((col, row))
                      if c == nodeid else None))
    return res[0]

def get_legs(nodeid, xcoord, ycoord):
    global LEGS_FOR_NODE, NUMBER_OF_LEGS

    if nodeid is None:
        nodeid = MAP[ycoord][xcoord]

    LEGS_FOR_NODE[nodeid] = []
    NUMBER_OF_LEGS = 0
    for direction in [1, -1]:
        for _, (deltax, deltay) in AXIS.items():
            (xcoord, ycoord) = find_node(nodeid)
            xcoord += deltax * direction
            ycoord += deltay * direction
            cost = 0
            leg_pheromone = 0
            while is_leg(xcoord, ycoord):
                cost += get_leg_cost(xcoord, ycoord)
                leg_pheromone += PHEROMONE_MAP[ycoord][xcoord]
                xcoord += deltax * direction
                ycoord += deltay * direction
            if is_node(xcoord, ycoord) and cost > 0:
                LEGS_FOR_NODE[nodeid].append(
                    (NUMBER_OF_LEGS, (deltax * direction, deltay * direction),
                     cost, leg_pheromone))
                NUMBER_OF_LEGS += 1
#            else:
#                warn('Neither leg nor node {:d} {:d} for node {:s}'.format(xcoord, ycoord, nodeid))

    return LEGS_FOR_NODE[nodeid]


# Pheromone functions
# ===================

def deposit_pheromone(x, y):
    if is_leg(x, y):
        PHEROMONE_MAP[y][x] += PHEROMONE
    else:
        warn("Cannot deposit pheromone on {:d}, {:d} since it isn't a leg".format(
             x, y))

def get_pheromone(x, y):
    return PHEROMONE_MAP[y][x]

def evaporate():
    for y in range(0, len(PHEROMONE_MAP)):
        for x in range(0, len(PHEROMONE_MAP[y])):
            if is_leg(x, y):
                PHEROMONE_MAP[y][x] *= EVAPORATION
