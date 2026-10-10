import unittest

from app.pricing import admin_fee, cb_index, financial_status, total_cost


class PricingTests(unittest.TestCase):
    def test_admin_fee_ranges_used_by_project(self):
        self.assertEqual(admin_fee(1405), 484.0)
        self.assertEqual(admin_fee(1985), 484.0)
        self.assertEqual(admin_fee(2000), 773.0)

    def test_total_cost(self):
        self.assertEqual(total_cost(1405), 1959.25)
        self.assertEqual(total_cost(1985), 2568.25)
        self.assertEqual(total_cost(2000), 2873.00)

    def test_financial_status(self):
        self.assertEqual(financial_status(1500, 2000), "ATRATIVO")
        self.assertEqual(financial_status(1950, 2000), "NO LIMITE")
        self.assertEqual(financial_status(2100, 2000), "ACIMA DO TETO")

    def test_cb_index_is_bounded_by_scoring_formula(self):
        score = cb_index(5000, 3000, 9.0, 7.0)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 10)


if __name__ == "__main__":
    unittest.main()
