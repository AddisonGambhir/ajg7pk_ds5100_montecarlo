import unittest
import numpy as np
from montecarlo import Die, Game, Analyzer
import sys


class TestDieGameAnalyzer(unittest.TestCase):

    # Test methods for Die class
    def test_die_creation(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        self.assertIsNotNone(die)

    def test_set_weight(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        die.set_weight(3, 5)
        self.assertEqual(die.get_die_state().loc[3, 'Weights'], 5)

    def test_roll(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        outcomes = die.roll(5)
        self.assertEqual(len(outcomes), 5)

    def test_get_die_state(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        state = die.get_die_state()
        self.assertTrue((state.index == faces).all())

    # Test methods for Game class
    def test_game_creation(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        self.assertIsNotNone(game)

    def test_game_play(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        self.assertEqual(game.play_data.shape[0], 5)

    def test_show_results(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        results = game.show_results('wide')
        self.assertEqual(results.shape[0], 5)

    # Test methods for Analyzer class
    def test_analyzer_creation(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        analyzer = Analyzer(game)
        self.assertIsNotNone(analyzer)

    def test_analyzer_jackpot(self):
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        game = Game([die1, die2])
        game.play(10)
        analyzer = Analyzer(game)
        self.assertTrue(analyzer.jackpot() >= 0)

    def test_analyzer_face_counts_per_roll(self):
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        game = Game([die1, die2])
        game.play(10)
        analyzer = Analyzer(game)
        counts = analyzer.face_counts_per_roll()
        self.assertEqual(counts.shape[0], 10)

    def test_analyzer_combo_count(self):
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        game = Game([die1, die2])
        game.play(10)
        analyzer = Analyzer(game)
        combos = analyzer.combo_count()
        self.assertTrue(combos.shape[0] > 0)

    def test_analyzer_permutation_count(self):
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        game = Game([die1, die2])
        game.play(10)
        analyzer = Analyzer(game)
        permutations = analyzer.permutation_count()
        self.assertTrue(permutations.shape[0] > 0)

# Execute the tests
#if __name__ == '__main__':
#    unittest.main()
#this command didn't push the results of the test to the .txt file so I had to check stack overflow

if __name__ == '__main__':
    unittest.TextTestRunner(stream=sys.stdout).run(unittest.TestLoader().loadTestsFromTestCase(TestDieGameAnalyzer))
