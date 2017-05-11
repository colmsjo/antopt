# pylint: disable=missing-docstring, global-statement
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)

# Imports
# ======

import unittest
import map_funcs


# Unit tests
# ==========

class TestMap(unittest.TestCase):

    def setUp(self):
        print('Testing map_funcs...')
        map_funcs.open_map('MAP1.txt')

    def test_map(self):
        self.assertTrue(map_funcs.is_node(0, 0))
        self.assertFalse(map_funcs.is_leg(0, 0))
        self.assertTrue(map_funcs.is_leg(1, 1))
        self.assertTrue(map_funcs.get_leg_cost(0, 1) == 1)
        self.assertTrue(len(map_funcs.get_nodes()) == 4)
        self.assertTrue(map_funcs.find_node('c') == (5, 5))
        self.assertTrue((map_funcs.get_legs('c', None, None) ==
                         [(0, (-1, 0), 4, 4.0), (1, (0, -1), 4, 4.0),
                          (2, (-1, -1), 4, 4.0)]))

    def test_pheromone(self):
        for x in range(1, 5):
            map_funcs.deposit_pheromone(x, 0)

        map_funcs.evaporate()

        for x in range(1, 5):
            self.assertTrue(map_funcs.get_pheromone(x, 0) == 1.8)

    def tearDown(self):
        print('...done with test.')


# Main
# ====

if __name__ == '__main__':
    unittest.main()
