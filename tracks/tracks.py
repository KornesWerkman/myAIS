import pathlib
import uuid
from datetime import datetime, timezone
from time import sleep

import tomllib

global TRACKS

toml_file = pathlib.PurePath(__file__).with_suffix(".toml")

if not pathlib.Path(toml_file).exists():
    raise FileNotFoundError(f"Configuration file {toml_file} not found")

with open(toml_file, "rb") as configs:
    TRACKS = tomllib.load(configs)


class CommonNavigationBlock:
    """Class that handles the common navigation block, the first 3 fields
    of any VDO/VDM message:
     - The Message ID
     - The Repeat indicator
     - The User ID (or source ID, MMSI)

    This class adds some meta data as well, such as:
     - A UUID for each target
     - Creation time, update time and age
    """

    mmsis: list = []
    msg_received: dict = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
        16: 0,
        17: 0,
        18: 0,
        19: 0,
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        24: 0,
        25: 0,
        26: 0,
        27: 0,
    }

    def __init__(self, user_id: str) -> None:
        self._user_id = user_id

        self._track_id: str = uuid.uuid4()
        self._ts_created = datetime.now(timezone.utc)
        self._updates: int = 0

        CommonNavigationBlock.mmsis.append(self._user_id)

    @property
    def age(self) -> int:
        return datetime.now(timezone.utc) - self._ts_created

    @property
    def message_id(self) -> int:
        return self._message_id

    @message_id.setter
    def message_id(self, value: int) -> None:
        self._message_id = int(value)

        self._ts_updated = datetime.now(timezone.utc)
        self._updates += 1

        CommonNavigationBlock.msg_received[self._message_id] += 1

    @property
    def repeat_indicator(self) -> int:
        return self._repeat_indicator

    @repeat_indicator.setter
    def repeat_indicator(self, value: int) -> None:
        self._repeat_indicator = int(value)

    @property
    def track_id(self) -> str:
        return str(self._track_id)

    @property
    def ts_created(self) -> str:
        return str(self._ts_created.isoformat("T"))

    @property
    def ts_updated(self) -> str:
        return str(self._ts_updated.isoformat("T"))

    @property
    def user_id(self) -> str:
        return self._user_id

    @classmethod
    def msg_statistics(cls) -> str:
        """Method that prints a bar diagram displaying the how many
        of each message type were received

        Sample output:
            Number of sentences received: 20
            Number of unique MMSIs: 16
            Message 1 : |#######                                           | 15% (3)
            Message 2 : |                                                  | 0% (0)
            ...
        """

        width = 50
        tnom = sum(cls.msg_received.values())
        _msg_statistics = f"Number of sentences received: {tnom}\n"
        _msg_statistics += f"Number of unique MMSIs: {len(cls.mmsis)}\n"
        _msg_statistics += f"{('-' * 78)}\n"
        for k, v in cls.msg_received.items():
            _msg_statistics += f"Message {k:<2}: "
            _msg_statistics += f"|{'#' * (int(width * (v / tnom))):<{width}s}| "
            _msg_statistics += f"{v / tnom:.0%} ({v})\n"
        return _msg_statistics

    def __str__(self) -> str:
        return (
            f"MMSI: {self._user_id}, Track ID: {self.track_id}\n"
            f"Time created: {self.ts_created}, updated: {self.ts_updated}, age: {self.age}\n"
            f"Message ID: {self._message_id}, Repeat indicator: {self._repeat_indicator}\n"
        )


class Target(CommonNavigationBlock):
    def __init__(self, user_id) -> None:
        super().__init__(user_id)

    @property
    def course_over_ground(self) -> float:
        return self._course_over_ground

    @course_over_ground.setter
    def course_over_ground(self, value) -> None:
        self._course_over_ground = float(value)

    @property
    def itdma_keep_flags(self) -> bool:
        return self._itdma_keep_flags

    @itdma_keep_flags.setter
    def itdma_keep_flags(self, value) -> None:
        self._itdma_keep_flags = bool(value)

    @property
    def itdma_number_of_slots(self) -> int:
        return self._itdma_number_of_slots

    @itdma_number_of_slots.setter
    def itdma_number_of_slots(self, value) -> None:
        self._itdma_number_of_slots = int(value)

    @property
    def itdma_slot_increment(self) -> int:
        return self._itdma_slot_increment

    @itdma_slot_increment.setter
    def itdma_slot_increment(self, value) -> None:
        self._itdma_slot_increment = int(value)

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value) -> None:
        self._latitude = float(value)

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value) -> None:
        self._longitude = float(value)

    @property
    def navigational_status(self) -> int:
        return self._navigational_status

    @navigational_status.setter
    def navigational_status(self, value) -> None:
        self._navigational_status = int(value)

    @property
    def position_accuracy(self) -> bool:
        return self._position_accuracy

    @position_accuracy.setter
    def position_accuracy(self, value) -> None:
        self._position_accuracy = bool(value)

    @property
    def raim(self) -> bool:
        return self._raim

    @raim.setter
    def raim(self, value) -> None:
        self._raim = bool(value)

    @property
    def rate_of_turn(self) -> float:
        return self._rate_of_turn

    @rate_of_turn.setter
    def rate_of_turn(self, value) -> None:
        self._rate_of_turn = float(value)

    @property
    def sotdma_spare(self) -> str:
        return self._sotdma_spare

    @sotdma_spare.setter
    def sotdma_spare(self, value) -> None:
        self._sotdma_spare = str(value)

    @property
    def sotdma_slot_number(self) -> int:
        return self._sotdma_slot_number

    @sotdma_slot_number.setter
    def sotdma_slot_number(self, value) -> None:
        self._sotdma_slot_number = int(value)

    @property
    def sotdma_slot_offset(self) -> int:
        return self._sotdma_slot_offset

    @sotdma_slot_offset.setter
    def sotdma_slot_offset(self, value) -> None:
        self._sotdma_slot_offset = int(value)

    @property
    def sotdma_slot_time_out(self) -> int:
        return self._sotdma_slot_time_out

    @sotdma_slot_time_out.setter
    def sotdma_slot_time_out(self, value) -> None:
        self._sotdma_slot_time_out = int(value)

    @property
    def sotdma_utc_hour(self) -> int:
        return self._sotdma_utc_hour

    @sotdma_utc_hour.setter
    def sotdma_utc_hour(self, value) -> None:
        self._sotdma_utc_hour = int(value)

    @property
    def sotdma_utc_minute(self) -> int:
        return self._sotdma_utc_minute

    @sotdma_utc_minute.setter
    def sotdma_utc_minute(self, value) -> None:
        self._sotdma_utc_minute = int(value)

    @property
    def spares(self) -> list:
        return self._spares

    @spares.setter
    def spares(self, value) -> None:
        self._spares = list(value)

    @property
    def special_manouvre_indicator(self) -> int:
        return self._special_manouvre_indicator

    @special_manouvre_indicator.setter
    def special_manouvre_indicator(self, value) -> None:
        self._special_manouvre_indicator = int(value)

    @property
    def speed_over_ground(self) -> float:
        return self._speed_over_ground

    @speed_over_ground.setter
    def speed_over_ground(self, value) -> None:
        self._speed_over_ground = float(value)

    @property
    def time_stamp(self) -> int:
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value) -> None:
        self._time_stamp = int(value)

    @property
    def true_heading(self) -> int:
        return self._true_heading

    @true_heading.setter
    def true_heading(self, value) -> None:
        self._true_heading = int(value)

    def __str__(self) -> str:
        return (
            f"MMSI: {self._user_id}, Track ID: {self.track_id}\n"
            f"Time created: {self.ts_created}, updated: {self.ts_updated}, age: {self.age}\n"
            f"Message ID: {self.message_id}, Repeat indicator: {self.repeat_indicator}\n"
            f"Navigation status: {self.navigational_status}, \n"
            f"Rate of turn (ROT): {self.rate_of_turn}, \n"
        )


if __name__ == "__main__":
    # -- --------------------------------------------------------------------------
    # -- messages borrowed from https://www.maritec.co.za/aisvdmvdodecoding
    # --
    messages: list = [
        "000001000011111101001111101101111100100000111110000010001011000000110110001010101100010100100000111111100101011101000001100101000001010011101010000000000110001001010100",
        "000100000000000000100100101011101100110001111101110001100100000111100110010100100010001110000011110110011001101110111010000110001110110001000000000000000000000000000000",
        "000101001000111111111100001000100101110001101000101111001111001111111010000010000001101000000111100011001101001010000010000010000000000101001000001100111110000000000101011000111100111000000000000000000000000000000000000000000000000001000101001110001000011111010001001011000000111011110011",
        "101101100001001000001000000010000011110101010100110101000011110011100000000000000000000000000000000000000000000000000000000000000000000000",
        "000110001110110010100010000000000110000000000000100110001010010011000000001110101100101001000100100000000001000000000110100000000000000000",
        "000110000001101011000010001011111001011100100000011000000001110101010000111111111011110101000110010001100010110000111000001100110010110001000110010001100100011000101100001100010011001000101110001101010010110000110011001110000011000100110011001011100011001000110001001101000011100100110111",
        "010100110010110000110001001101000011010100110001001100000010111000111000001101000011000100110011001110000100010100",
        "001000001110110000001000110110110011100000000000010111110100111010001101001100110000010110011001000000010100000110001111001111111111111110110100010110100010000000000110010101111101011111111111101111111111110100001111111111110110100011111111101101000111111111111110110100011111111111001111111011010001111111111111110110100011010111110101111111111110110000000000",
        "001001000101011101000010110111100001010000000100000001100100111010000100011100000100011000010000101101100010111110100001001011000010110000000010000000000000000000000000",
        "001011001000111101001010001000010011010001111101110001100100000111010010110101000010010011011001011101001101101110111011010100011010000001000000000000000000000000000000",
        "001110001110011101000100101110100111010001001100000101001001010010000001010000010101001101010000",
        "010010000110010011101100010011110101000000111100000011101000111100101010101001000011000101101110010000100110001001101110101001011000110001000111110011100000000000000110",
        "010011001000111101001010001000010011010000111100000111010000100100110110010111010011011011101110110101000110100000110111101000101101000110011110101000001010100110101001000000011100000010011010001011000000000110011000100110000101000000011010100110001111100011110010010010100000011100000011",
        "000001000001100010100000",
        "010101000001101011000010001011111001010000101010000100000100101001110000000100101001110000000000110000001010000010101001101010010000000111000000100110100010111000100101001100010010101111111000110101000100001010101111100000000101000000011000011000101000100100110000101000100001010110000101",
        "000001010011100001000001010001001000000011100000010011010001011000000000",
        "011000000001101011000010001011111001010001010000100000100101001110000000100101001110000000000110000000001100110000000101001101001110000000001010000001010100111000",
        "011000000001101011000010001011111001010100100100110001110010110011110100110101110110110111000011000001001100001100010011001001000111000000101000000100000011001100000001",
        "011011010011100001001001111010001101110000111010010110100101110110011000000111100000000000000000",
        "011011010011000101010101000010101010010000100101000001001001100000010110101100011100101010011101111101101011000101001101100010011111111110000110000010001100000111110101",
        "011011000101010100101110011101010010001001010110011100111011011101001111100000000000000000101100",
    ]

    targets = {}
    for message in messages:
        if len(message) >= 38:
            message_id: int = int(message[0:6], 2)
            if message_id <= 27 and message_id >= 1:
                repeat_indicator: int = int(message[6:8], 2)
                mmsi: str = f"{int(message[8:38], 2):09d}"
                if mmsi not in targets.keys():
                    targets[mmsi] = Target(mmsi)
                targets[mmsi].message_id = message_id
                targets[mmsi].repeat_indicator = repeat_indicator
                targets[mmsi].navigational_status = int(message[38:42], 2)
                targets[mmsi].rate_of_turn = int(message[42:50], 2)
                print(targets[mmsi])
                sleep(0.5)

    print(CommonNavigationBlock.msg_statistics())
