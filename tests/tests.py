import glicko2
import unittest

class testCases(unittest.TestCase):

    def setUp(self):
        # Feb222012 example.
        self.P1 = glicko2.Player()
        self.P1.setRd(200)
        self.P1.update_player([1400, 1550, 1700], [30, 100, 300], [1, 0, 0])
        # Original Ryan example.
        self.Ryan = glicko2.Player()
        self.Ryan.update_player([1400, 1550, 1700],
           [30, 100, 300], [1, 0, 0])


    def test_rating(self):
        self.assertEqual(round(self.P1.rating, 2), 1464.05)

    def test_ratingDeviation(self):
        self.assertEqual(round(self.P1.rd, 2), 151.52)

    def test_volatility(self):
        # the paper prints 0.05999 (truncated); the exact value is 0.059996
        self.assertAlmostEqual(self.P1.vol, 0.05999, places=4)

    def test_ryan_rating(self):
        self.assertEqual(round(self.Ryan.rating, 2), 1441.53)

    def test_ryan_ratingDeviant(self):
        self.assertEqual(round(self.Ryan.rd, 2), 193.23)

    def test_ryan_volatility(self):
        self.assertAlmostEqual(self.Ryan.vol, 0.05999, places=4)

    def test_volatility_solver_uses_rating_deviation(self):
        # Step 5.1's f(x) has the player's rating deviation (phi) in it, not the rating (mu). The paper's example is
        # nearly blind to the difference (it moves the volatility by 2e-6), so use a surprising result, where the
        # error reaches 0.02 rating points. Expected values are a direct transcription of the paper's algorithm.
        player = glicko2.Player(1500, 30, 0.06)
        player.update_player([2000] * 12, [30] * 12, [1] * 12)
        self.assertAlmostEqual(player.rating, 1564.7259, places=3)
        self.assertAlmostEqual(player.rd, 31.5414, places=3)
        self.assertAlmostEqual(player.vol, 0.061773, places=5)

    def test_volatility_solver_with_a_player_away_from_1500(self):
        player = glicko2.Player(1700, 150, 0.06)
        player.update_player([1400, 1550, 1500], [30, 100, 300], [1, 0, 0])
        self.assertAlmostEqual(player.rating, 1600.05787, places=4)
        self.assertAlmostEqual(player.rd, 130.72658, places=4)
        self.assertAlmostEqual(player.vol, 0.0600036, places=6)

if __name__ == "__main__":
    unittest.main()
