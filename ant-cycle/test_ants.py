# pylint: disable=missing-docstring, global-statement
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)

# Imports
# ======

import unittest
import ants
import map_funcs


# Setup logging
# =============

DEBUG_MODE = True

def debug(*args):
    print('DEBUG:test_ants:', *args)

def error(*args):
    print('ERROR:test_ants:', *args)

def warn(*args):
    print('WARNING:test_ants:', *args)


# Unit tests
# ==========

class TestAnts(unittest.TestCase):

    def setUp(self):
        print('Testing ants...')
        ants.init('MAP2.txt')

    def test_calc_probabilities(self):
        debug('test_calc_probabilities')
        for antno in range(0, ants.NO_OF_ANTS):
            probs = ants.calc_transition_probabilities(antno)

            # Check that the probabilities add upp
            total = 0
            for p in probs:
                total += p[2]
            self.assertTrue(total == 1.0)

    def test_select_random_leg(self):
        debug('test_select_random_leg')
        probs = ants.calc_transition_probabilities(0)
        probs.sort(key=lambda x: 1-x[2])                # just for readability

        # Check that the edges most often selected are the ones with highest
        # probability
        selected_edge = {}
        for _ in range(0, 1000):
            (node1, node2, _) = ants.select_random_edge(probs)
            if node1 + node2 in selected_edge:
                selected_edge[node1 + node2] += 1
            else:
                selected_edge[node1 + node2] = 1

        selected_edge = list(selected_edge.items())
        selected_edge.sort(key=lambda x: x[1], reverse=True)

        self.assertTrue(selected_edge[0][0] == 'ag' or selected_edge[0][0] == 'ad')

    @staticmethod
    def test_move():
        debug('test_move')
        for antno in range(0, ants.NO_OF_ANTS):
            for _ in range(0, len(map_funcs.EDGES)):
                if not ants.all_nodes_visited(antno):
                    ants.move(antno)

            ants.deposition_pheromone_it(antno)

        ants.sort_ants()

    def tearDown(self):
        print('...done with test.')

# Main
# ====

if __name__ == '__main__':
    unittest.main()
