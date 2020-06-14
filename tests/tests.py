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
        self.assertEqual(round(self.P1.vol, 5), 0.05999)

    def test_ryan_rating(self):
        self.assertEqual(round(self.Ryan.rating, 2), 1441.53)

    def test_ryan_ratingDeviant(self):
        self.assertEqual(round(self.Ryan.rd, 2), 193.23)

    def test_ryan_volatility(self):
        self.assertEqual(round(self.Ryan.vol, 5), 0.05999)

if __name__ == "__main__":
    unittest.main()
