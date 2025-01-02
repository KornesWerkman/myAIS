import unittest

import ais

message = "The output unexpectedly is not equal"


class TestCheckTheBits(unittest.TestCase):
    def test_check_the_bits(self):
        bits: str = "0101"
        result: str = "0101"
        self.assertEqual(ais.check_the_bits(bits, len(bits)), result, message)

    def test_check_the_bits_0b(self):
        bits: str = "0b0101"
        result: str = "0101"
        self.assertEqual(ais.check_the_bits(bits, len(bits) - 2), result, message)

    def test_check_the_bits_invalid_char(self):
        bits: str = "0b010123"
        result: str = "010123"
        with self.assertRaises(ValueError):
            self.assertEqual(ais.check_the_bits(bits, len(bits) - 2), result)

    def test_check_the_bits_invalid_length(self):
        bits: str = "0b0101"
        result: str = "0101"
        with self.assertRaises(ValueError):
            self.assertEqual(ais.check_the_bits(bits, len(bits)), result)


class TestDecodeCourseOverGround(unittest.TestCase):
    """The course over ground ranges from 0 - 359,9 degrees and is delivered in 12 bits
    special value is at 3600. Any readout exceeding this is invalid
    """

    def test_decode_course_over_ground(self):
        cog: str = "000000000000"
        result: dict = {"value": 0.0, "valid": True, "unit": "degrees"}
        self.assertEqual(ais.decode_course_over_ground(cog), result, message)

    def test_decode_course_over_ground_3600(self):
        cog: str = f"{bin(3600)[2:]:0>12}"
        result: dict = {"value": 3600, "valid": True, "state": "Not available, default"}
        self.assertEqual(ais.decode_course_over_ground(cog), result, message)

    def test_decode_course_over_ground_11_bits(self):
        cog: str = "00000000000"
        result: dict = {"value": 0.0, "valid": True, "unit": "degrees"}
        with self.assertRaises(ValueError):
            self.assertEqual(ais.decode_course_over_ground(cog), result)

    def test_decode_course_over_ground_13_bits(self):
        cog: str = "0000000000000"
        result: dict = {"value": 0.0, "valid": True, "unit": "degrees"}
        with self.assertRaises(ValueError):
            self.assertEqual(ais.decode_course_over_ground(cog), result)

    def test_decode_course_over_ground_out_of_range(self):
        cog: str = "111111111111"
        result: dict = {"value": 4095, "valid": False}
        self.assertEqual(ais.decode_course_over_ground(cog), result, message)


class TestDecodeRateOfTurn(unittest.TestCase):
    def test_decode_rate_of_turn(self):
        rot: str = "00000000"
        result: dict = {
            "value": 0,
            "description": "Not turning",
            "unit": "degrees/minute",
        }
        self.assertEqual(ais.decode_rate_of_turn(rot), result, message)

    def test_decode_rate_of_turn_hard_right(self):
        rot: str = "01111111"
        result: dict = {
            "value": 127,
            "description": "Turning right at more than 5° per 30 s (No TI available)",
            "unit": "degrees/minute",
        }
        self.assertEqual(ais.decode_rate_of_turn(rot), result, message)

    def test_decode_rate_of_turn_hard_left(self):
        rot: str = "10000001"
        result: dict = {
            "value": -127,
            "description": "Turning left at more than 5° per 30 s (No TI available)",
            "unit": "degrees/minute",
        }
        self.assertEqual(ais.decode_rate_of_turn(rot), result, message)

    def test_decode_rate_of_turn_no_rot(self):
        rot: str = "10000000"
        result: dict = {
            "value": -128,
            "description": "No turn information available, default",
            "unit": "degrees/minute",
        }
        self.assertEqual(ais.decode_rate_of_turn(rot), result, message)

    def test_decode_rate_of_turn_right(self):
        rot: str = "01111110"
        result: dict = {
            "value": 708.7092175811848,
            "description": "Turning to starboard",
            "unit": "degrees/minute",
        }
        self.assertEqual(ais.decode_rate_of_turn(rot), result, message)

    def test_decode_rate_of_turn_left(self):
        rot: str = "10000010"
        result: dict = {
            "value": -708.7092175811848,
            "description": "Turning to port",
            "unit": "degrees/minute",
        }
        self.assertEqual(ais.decode_rate_of_turn(rot), result, message)

    def test_decode_rate_of_turn_too_few_bits(self):
        rot: str = "1111111"
        with self.assertRaises(ValueError):
            ais.decode_rate_of_turn(rot)

    def test_decode_rate_of_turn_too_many_bits(self):
        rot: str = "111111111"
        with self.assertRaises(ValueError):
            ais.decode_rate_of_turn(rot)

    def test_decode_rate_of_turn_wrong_input(self):
        rot: str = "abcdefgh"
        with self.assertRaises(ValueError):
            ais.decode_rate_of_turn(rot)


class TestPayloadToBinary(unittest.TestCase):
    def test_payload_to_binary(self):
        """Test if supported characters are correctly translated"""
        payload: str = "1"
        binary: str = "000001"
        self.assertEqual(ais.payload_to_binary(payload), binary, message)

    def test_payload_to_binary_all(self):
        """Test if supported characters are correctly translated"""
        i = 0
        for payload in ais.payload_chars:
            binary = f"{bin(i).lstrip('0b'):0>6}"
            self.assertEqual(ais.payload_to_binary(payload), binary, message)
            i += 1

    def test_payload_to_binary_2(self):
        """Test if unsupported characters raise a ValueError"""
        payload: str = "x"  # does not exist in the set
        with self.assertRaises(ValueError):
            ais.payload_to_binary(payload)


class TestDecodePositions(unittest.TestCase):
    def test_decode_position(self):
        """Test if positions are correctly converted"""
        longitude: str = 28 * "0"
        latitude: str = 27 * "0"
        position: dict = {
            "longitude": {"value": "000* 0.0000' E", "valid": True, "state": None},
            "latitude": {"value": "00* 0.0000' N", "valid": True, "state": None},
            "geopos": (0.0, 0.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_max_lat(self):
        """Test if positions are correctly converted"""
        longitude: str = 28 * "0"
        latitude: str = f"{bin(90 * 600_000)[2:]:0>27}"
        position: dict = {
            "longitude": {"value": "000* 0.0000' E", "valid": True, "state": None},
            "latitude": {"value": "90* 0.0000' N", "valid": True, "state": None},
            "geopos": (0.0, 90.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_max_long(self):
        """Test if positions are correctly converted"""
        longitude: str = f"{bin(180 * 600_000)[2:]:0>28}"
        latitude: str = 27 * "0"
        position: dict = {
            "longitude": {"value": "180* 0.0000' E", "valid": True, "state": None},
            "latitude": {"value": "00* 0.0000' N", "valid": True, "state": None},
            "geopos": (180.0, 0.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_default_lat(self):
        """Test if positions are correctly converted"""
        longitude: str = 28 * "0"
        latitude: str = f"{bin(91 * 600_000)[2:]:0>27}"
        position: dict = {
            "longitude": {"value": "000* 0.0000' E", "valid": True, "state": None},
            "latitude": {
                "value": "91* 0.0000' N",
                "valid": True,
                "state": "Not available, default",
            },
            "geopos": (0.0, 91.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_default_long(self):
        """Test if positions are correctly converted"""
        longitude: str = f"{bin(181 * 600_000)[2:]:0>28}"
        latitude: str = 27 * "0"
        position: dict = {
            "longitude": {
                "value": "181* 0.0000' E",
                "valid": True,
                "state": "Not available, default",
            },
            "latitude": {"value": "00* 0.0000' N", "valid": True, "state": None},
            "geopos": (181.0, 0.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_very_max_lat(self):
        """Test if positions are correctly converted"""
        longitude: str = 28 * "0"
        latitude: str = "0" + 26 * "1"
        position: dict = {
            "longitude": {"value": "000* 0.0000' E", "valid": True, "state": None},
            "latitude": {"value": "111* 50.8863' N", "valid": False, "state": None},
            "geopos": (0.0, 111.848105),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_very_max_long(self):
        """Test if positions are correctly converted"""
        longitude: str = "0" + 27 * "1"
        latitude: str = 27 * "0"
        position: dict = {
            "longitude": {"value": "223* 41.7727' E", "valid": False, "state": None},
            "latitude": {"value": "00* 0.0000' N", "valid": True, "state": None},
            "geopos": (223.69621166666667, 0.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_min_lat(self):
        """Test if positions are correctly converted"""
        longitude: str = 28 * "0"
        latitude: str = "100110010000000011010000000"  # -90 * 60,000
        position: dict = {
            "longitude": {"value": "000* 0.0000' E", "valid": True, "state": None},
            "latitude": {"value": "90* 0.0000' S", "valid": True, "state": None},
            "geopos": (0.0, -90.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)

    def test_decode_position_min_long(self):
        """Test if positions are correctly converted"""
        longitude: str = "1001100100000000110100000000"  # -180 * 60,000
        latitude: str = 27 * "0"
        position: dict = {
            "longitude": {"value": "180* 0.0000' W", "valid": True, "state": None},
            "latitude": {"value": "00* 0.0000' N", "valid": True, "state": None},
            "geopos": (-180.0, 0.0),
        }

        self.assertEqual(ais.decode_position(longitude, latitude), position, message)


class TestDecodeTimeStamp(unittest.TestCase):
    """Test if timestamps are converted correctly"""

    def test_decode_time_stamp(self):
        th: str = 6 * "1"
        result: dict = {
            "value": 63,
            "description": "Positioning system is inoperative",
            "unit": "seconds (UTC)",
        }
        self.assertDictEqual(ais.decode_time_stamp(th), result, message)

    # def test_decode_true_heading_max(self):
    #     th: str = 9 * "1"
    #     result: dict = {
    #         "value": 511,
    #         "unit": "degrees",
    #         "valid": "Not available, default",
    #     }
    #     self.assertDictEqual(ais.decode_time_stamp(th), result, message)

    # def test_decode_true_heading_max_valid(self):
    #     th: str = f"{bin(359)[2:]:0>9}"
    #     result: dict = {"value": 359, "unit": "degrees", "valid": True}
    #     self.assertDictEqual(ais.decode_time_stamp(th), result, message)

    # def test_decode_true_heading_min_invalid(self):
    #     th: str = f"{bin(360)[2:]:0>9}"
    #     result: dict = {"value": 360, "unit": "degrees", "valid": False}
    #     self.assertDictEqual(ais.decode_time_stamp(th), result, message)

    # def test_decode_true_heading_too_short(self):
    #     th: str = 8 * "1"
    #     with self.assertRaises(ValueError):
    #         self.assertEqual(ais.decode_time_stamp(th))

    # def test_decode_true_heading_too_long(self):
    #     th: str = 5 * "10"
    #     with self.assertRaises(ValueError):
    #         self.assertEqual(ais.decode_time_stamp(th))

    # def test_decode_true_heading_wrong_input(self):
    #     th: str = "aBcDeFgHi"
    #     with self.assertRaises(ValueError):
    #         self.assertEqual(ais.decode_time_stamp(th))


class TestDecodeTrueHeading(unittest.TestCase):
    """Test if headings are converted correctly"""

    def test_decode_true_heading(self):
        th: str = 9 * "0"
        result: dict = {"value": 0, "unit": "degrees", "valid": True}
        self.assertDictEqual(ais.decode_true_heading(th), result, message)

    def test_decode_true_heading_max(self):
        th: str = 9 * "1"
        result: dict = {
            "value": 511,
            "unit": "degrees",
            "valid": "Not available, default",
        }
        self.assertDictEqual(ais.decode_true_heading(th), result, message)

    def test_decode_true_heading_max_valid(self):
        th: str = f"{bin(359)[2:]:0>9}"
        result: dict = {"value": 359, "unit": "degrees", "valid": True}
        self.assertDictEqual(ais.decode_true_heading(th), result, message)

    def test_decode_true_heading_min_invalid(self):
        th: str = f"{bin(360)[2:]:0>9}"
        result: dict = {"value": 360, "unit": "degrees", "valid": False}
        self.assertDictEqual(ais.decode_true_heading(th), result, message)

    def test_decode_true_heading_too_short(self):
        th: str = 8 * "1"
        with self.assertRaises(ValueError):
            self.assertEqual(ais.decode_true_heading(th))

    def test_decode_true_heading_too_long(self):
        th: str = 5 * "10"
        with self.assertRaises(ValueError):
            self.assertEqual(ais.decode_true_heading(th))

    def test_decode_true_heading_wrong_input(self):
        th: str = "aBcDeFgHi"
        with self.assertRaises(ValueError):
            self.assertEqual(ais.decode_true_heading(th))
