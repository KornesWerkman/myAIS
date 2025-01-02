import unittest

import nmea


class TestCalculateCheckSum(unittest.TestCase):
    def test_calculate_check_sum(self):
        sentence: str = "!AIVDM,1,1,,A,13u?etPv2;0n:dDPwUM1U1Cb069D,0"
        checksum: str = "23"
        output = {"value": "0x23", "calculated": "0x24", "valid": False}
        message = "The output unexpectedly is not equal"
        self.assertEqual(nmea.calculate_check_sum(sentence, checksum), output, message)
