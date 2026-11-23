"""Never publish percentages from contradictory supply and wallet balances."""
import unittest
from unittest.mock import patch
import assets

class SupplyConsistencyTests(unittest.TestCase):
    def collect(self, balance):
        responses = [
            {'metadata': {'address': assets.MASTER_RAW, 'decimals': assets.DECIMALS},
             'total_supply': '1000000000'},
            {'total': 1, 'addresses': [{'owner': {'address': '0:'+'1'*64},
                                      'balance': str(balance)}]},
        ]
        with patch.object(assets, 'fetch', side_effect=responses):
            return assets.holders()

    def test_balance_above_supply_blocks_rankings(self):
        with self.assertRaises(assets.HolderSupplyMismatch):
            self.collect(1000000001)

    def test_consistent_supply_recovers_without_manual_override(self):
        data = self.collect(250000000)
        self.assertEqual(data['holders'][0]['share'], 25.0)
        self.assertEqual(data['totalSupply'], '1')

if __name__ == '__main__':
    unittest.main()
