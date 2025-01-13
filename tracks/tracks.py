import pathlib
import uuid
from datetime import datetime, timezone

import tomllib

global TRACKS

toml_file = pathlib.PurePath(__file__).with_suffix(".toml")

if not pathlib.Path(toml_file).exists():
    raise FileNotFoundError(f"Configuration file {toml_file} not found")

with open(toml_file, "rb") as configs:
    TRACKS = tomllib.load(configs)


class CommonNavigationBlock:
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

    def __str__(self) -> str:
        return (
            f"MMSI: {self._user_id}, Track ID: {self.track_id}\n"
            f"Time created: {self.ts_created}, updated: {self.ts_updated}, age: {self.age}\n"
            f"Message ID: {self._message_id}, Repeat indicator: {self._repeat_indicator}\n"
        )


class Track(CommonNavigationBlock):
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
tracks = {}
mmsi = "265547250"
tracks[mmsi] = Track(mmsi)
tracks[mmsi].message_id = 1
tracks[mmsi].repeat_indicator = 1

print(tracks[mmsi])
