import unittest
from src.main import calculate_installment


class TestInstallmentCalculation(unittest.TestCase):
    def test_calculate_installment(self):
        asset_value = 30000.0
        duration = 60
        admin_fee_total = 15.0
        reserve_fund_total = 2.0
        seguro = 9.99
        installment = calculate_installment(
            asset_value,
            duration,
            admin_fee_total / 100,
            reserve_fund_total / 100,
            seguro,
        )
        self.assertAlmostEqual(installment, 594.99, places=2)


if __name__ == "__main__":
    unittest.main()
