import unittest
from unittest.mock import patch
import pools

class PoolIdentityTests(unittest.TestCase):
    def result(self):
        return {'included': [], 'data': [{
            'attributes': {'address': pools.REVIEWED_NON_NATIVE, 'reserve_in_usd': '2104.4167'},
            'relationships': {
                'base_token': {'data': {'id': 'ton_'+pools.NATIVE}},
                'quote_token': {'data': {'id': 'ton_'+pools.MASTER}},
                'dex': {'data': {'id': 'stonfi-v2'}}}}]}

    def test_dex_assets_replace_incorrect_native_quote(self):
        quote = 'EQDNhy-nxYFgUqzfUzImBEP67JqsyMIcyk2S5_RwNNEYku0k'
        answers = [self.result(), {'pool': {'token0_address': pools.MASTER,
                                          'token1_address': quote}},
                   {'metadata': {'symbol': 'stGRAM'}}]
        with patch.object(pools, 'fetch', side_effect=answers):
            row = pools.collect(2_000_000_000)['rows'][0]
        self.assertEqual(row['token'], quote)
        self.assertEqual(row['symbol'], 'stGRAM')

    def test_other_token_pool_is_rejected(self):
        answers = [self.result(), {'pool': {'token0_address': pools.NATIVE,
                                          'token1_address': pools.NATIVE}}]
        with patch.object(pools, 'fetch', side_effect=answers):
            with self.assertRaises(ValueError):pools.collect(2_000_000_000)
