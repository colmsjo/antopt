# pylint: disable=missing-docstring, global-statement
#
# [Using Google Style Guide](https://google.github.io/styleguide/pyguide.html)

# Imports
# ======

import unittest
import map_funcs
import ants

# Unit tests
# ==========

class TestAnts(unittest.TestCase):

    def setUp(self):
        print('Testing ants...')
        map_funcs.open_map('MAP1.txt')
        ants.init()

    def test_move(self):
        for antno in range(0, ants.NO_OF_ANTS):
            ants.move(antno)
            self.assertTrue(ants.get_ant(antno) in [((0, 1), (0, 1)),
                                                ((1, 0), (1, 0)),
                                                ((1, 1), (1, 1))])

    def tearDown(self):
        print('...done with test.')

# Main
# ====

if __name__ == '__main__':
    unittest.main()
