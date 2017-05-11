# pylint: disable=missing-docstring, global-statement
#
# NODES = {node1: (x, y), ..., nodeN}
# EDGES = {node1: {node2: distance, ..., nodeN: distance}, ..., nodeN{...}}
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)


# Imports
# =======

import sys

# Setup logging
# =============

def debug(*args):
    print('DEBUG:ants:', *args)

def error(*args):
    print('ERROR:ants:', *args)

def warn(*args):
    print('WARNING:ants:', *args)


# Map functions
# =============

NODES = {}
EDGES = {}

def open_map(filename):
    global NODES
    filehandle = open(filename)
    m = filehandle.read().split('\n')
    for i in range(0, len(m)):
        for j in range(0, len(m[i])):
            if m[i][j] != ' ':
                NODES[m[i][j]] = (j, i)

    filehandle.close()
    return NODES

def calc_distances():
    global NODES, EDGES

    # Initialize the EDGES
    for n in NODES:
        EDGES[n] = {}

    # Calculate distances
    for n in NODES:
        for m in NODES:
            if n != m:
                EDGES[n][m] = pow(pow(NODES[n][0]-NODES[m][0], 2) +
                                  pow(NODES[n][1]-NODES[m][1], 2), 0.5)

    return EDGES


# Main
# ====

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python map_funcs.py <MAP>', sys.argv)
        exit(0)

    open_map(sys.argv[1])
    calc_distances()

    print('\n\nCoordinates for nodes:', NODES)
    print('\n\nDistances betweeen nodes (edges):', EDGES)
