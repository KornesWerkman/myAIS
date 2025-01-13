import pathlib
import uuid
from datetime import datetime, timezone
import ais

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
     - Creation and update times
    """

    msg_received: dict = {
        "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0,
        "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0,
        "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0,
        "23": 0, "24": 0,"25": 0, "26": 0, "27": 0
    }

    def __init__(self, user_id: str) -> None:
        # -- Info from common navigation block
        self._user_id = user_id

        # -- Some meta info
        self._track_id: str = uuid.uuid4()
        self._ts_created = datetime.now(timezone.utc)

    @property
    def age(self) -> int:
        return abs(self._ts_created - datetime.now(timezone.utc))

    @property
    def message_id(self) -> int:
        return self._message_id

    @message_id.setter
    def message_id(self, value: int) -> None:
        self._ts_updated = datetime.now(timezone.utc)
        self._message_id = int(value)
        CommonNavigationBlock.msg_received[str(self._message_id)] += 1

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

    def msg_statistics() -> str:
        """ Method that prints a bar diagram displaying the how many
        of each message type were received
        """

        tnom = sum(
            CommonNavigationBlock.msg_received.values()
            )
        for k, v in CommonNavigationBlock.msg_received.items():
            print(f"Message {k:2}: ",
                  f"{"#"*(int(50 * (v / tnom)))} ",
                  f"{v / tnom:.0%} ({v})"
                  )


    def __str__(self) -> str:
        return (
            f"MMSI: {self._user_id}, Track ID: {self.track_id}\n"
            f"Time created: {self.ts_created}, updated: {self.ts_updated}, age: {self.age}\n"
            f"Message ID: {self._message_id}, Repeat indicator: {self._repeat_indicator}\n"
        )


class Target(CommonNavigationBlock):
    def __init__(
        self,
        user_id,
    ) -> None:
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


# -- --------------------------------------------------------------------------
# -- messages borrowed from https://www.maritec.co.za/aisvdmvdodecoding
# --

messages: list = [
    "!AIVDM,1,1,,A,13u?etPv2;0n:dDPwUM1U1Cb069D,0*23",
    "!AIVDM,1,1,,A,400TcdiuiT7VDR>3nIfr6>i00000,0*78",
    "!AIVDM,2,1,0,A,58wt8Ui`g??r21`7S=:22058<v05Htp000000015>8OA;0sk,0*7B",
    "!AIVDM,2,2,0,A,eQ8823mDm3kP00000000000,2*5D",
    "!AIVDM,1,1,4,B,6>jR0600V:C0>da4P106P00,2*02",
    "!AIVDM,2,1,9,B,61c2;qLPH1m@wsm6ARhp<ji6ATHd<C8f=Bhk>34k;S8i=3To,0*2C",
    "!AIVDM,2,2,9,B,Djhi=3Di<2pp=34k>4D,2*03",
    "!AIVDM,1,1,1,B,8>h8nkP0Glr=<hFI0D6??wvlFR06EuOwgwl?wnSwe7wvlOw?sAwwnSGmwvh0,0*17",
    "!AIVDO,1,1,,A,95M2oQ@41Tr4L4H@eRvQ;2h20000,0*0D",
    "!AIVDM,1,1,,B,;8u:8CAuiT7Bm2CIM=fsDJ100000,0*51",
    "!AIVDM,1,1,,B,>>M4fWA<59B1@E=@,0*17",
    "!AIVDM,1,1,,A,B6CdCm0t3`tba35f@V9faHi7kP06,0*58",
    "!AIVDM,2,1,0,B,C8u:8C@t7@TnGCKfm6Po`e6N`:Va0L2J;06HV50JV?SjBPL3,0*28",
    "!AIVDM,2,2,0,B,11RP,0*17",
    "!AIVDO,2,1,5,B,E1c2;q@b44ah4ah0h:2ab@70VRpU<Bgpm4:gP50HH`Th`QF5,0*7B",
    "!AIVDO,2,2,5,B,1CQ1A83PCAH0,0*60",
    "!AIVDO,1,1,,B,H1c2;qA@PU>0U>060<h5=>0:1Dp,2*7D",
    "!AIVDO,1,1,,B,H1c2;qDTijklmno31<<C970`43<1,0*28",
    "!AIVDM,1,1,,A,KCQ9r=hrFUnH7P00,0*41",
    "!AIVDM,1,1,,B,KC5E2b@U19PFdLbMuc5=ROv62<7m,0*16",
    "!AIVDM,1,1,,B,K5DfMB9FLsM?P00d,0*70"
]

for message in messages:
    payload = message.split(",")[5]
    # payload = ais.payload_to_binary(payload)
    print(payload)


targets = {}
mmsi = "265547250"
targets[mmsi] = Target(mmsi)
targets[mmsi].message_id = 1
targets[mmsi].repeat_indicator = 1

print(targets[mmsi])
CommonNavigationBlock.msg_statistics()
