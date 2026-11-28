import base64
import binascii
import unittest
import assets

class AddressTests(unittest.TestCase):
    def test_valid_friendly_address(self):
        self.assertEqual(assets.raw_address(assets.MASTER), assets.MASTER_RAW)

    def test_invalid_checksum(self):
        data = bytearray(base64.urlsafe_b64decode(assets.MASTER))
        data[-1] ^= 1
        with self.assertRaises(ValueError):
            assets.raw_address(base64.urlsafe_b64encode(data).decode())

    def test_raw_address(self):
        self.assertEqual(assets.raw_address("0:"+"AB"*32), "0:"+"ab"*32)

    def test_masterchain(self):
        data = bytes([0x51, 255]) + bytes(32)
        encoded = base64.urlsafe_b64encode(data + binascii.crc_hqx(data, 0).to_bytes(2, "big")).decode()
        self.assertEqual(assets.raw_address(encoded), "-1:"+"00"*32)
