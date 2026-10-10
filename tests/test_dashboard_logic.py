import unittest

from app.dashboard import bids_left, decision, risk_band


class DashboardLogicTests(unittest.TestCase):
    def test_decision(self):
        self.assertEqual(decision(1400, 2000, 100), "ATRATIVO")
        self.assertEqual(decision(1950, 2000, 100), "ÚLTIMO LANCE")
        self.assertEqual(decision(2100, 2000, 100), "ABANDONAR")

    def test_bids_left(self):
        self.assertEqual(bids_left(1400, 2000, 100), 7)
        self.assertEqual(bids_left(2100, 2000, 100), 0)

    def test_risk_band(self):
        self.assertEqual(risk_band(0.50, "ATRATIVO"), "good")
        self.assertEqual(risk_band(0.94, "ATRATIVO"), "attention")
        self.assertEqual(risk_band(0.99, "ÚLTIMO LANCE"), "last")
        self.assertEqual(risk_band(1.10, "ABANDONAR"), "dead")


if __name__ == "__main__":
    unittest.main()
