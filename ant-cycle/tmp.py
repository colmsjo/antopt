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
