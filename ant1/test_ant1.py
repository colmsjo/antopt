import unittest
import ant1

class TestAnt1(unittest.TestCase):

    def test_select_random_leg(self):
        i=0
        selected = [0] * 4
        while i < 100:
          legno = ant1.select_random_leg([(0, 0.1), (1, 0.2), (2, 0.3), (3, 0.4)])
          selected[legno] += 1
          i += 1

        # check that the selections are reasonable
        self.assertTrue(selected[0] <= selected[1] and
                        selected[1] <= selected[2] and
                        selected[2] <= selected[3])

if __name__ == '__main__':
    unittest.main()
