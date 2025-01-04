import unittest

from myAis import split_nmea


class TestMyAis(unittest.TestCase):
    def test_print(self):
        data = "!AIVDM,1,1,,A,13u?etPv2;0n:dDPwUM1U1Cb069D,0"
        check_sum = "23"
        output = {
            "delimiter": "!",
            "talker_id": "AI",
            "sentence_formatter": "VDM",
            "count_of_fragments": 1,
            "fragment_number": 1,
            "sequential_message_id": "",
            "ais_channel": "A",
            "payload": "13u?etPv2;0n:dDPwUM1U1Cb069D",
            "number_of_fill_bits": 0,
            "check_sum": "0x23",
        }
        message = "The output unexpectedly is not equal"
        self.assertEqual(split_nmea(data, check_sum), output, message)
