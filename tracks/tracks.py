from datetime import datetime, timezone

import pathlib

import tomllib

global TRACKS

toml_file = pathlib.PurePath(__file__).with_suffix(".toml")

if not pathlib.Path(toml_file).exists():
    raise FileNotFoundError(f"Configuration file {toml_file} not found")

with open(toml_file, "rb") as configs:
    TRACKS = tomllib.load(configs)


class CommonNavigationBlock():

    def __init__(self,
                 message_id: int,
                 repeat_indicator: int,
                 user_id: str) -> None:

        self.message_id = message_id
        self.repeat_indicator = repeat_indicator
        self.user_id = user_id

        self.ts_created = datetime.now(timezone.utc)


class Track(CommonNavigationBlock):
    def __init(self,
               course_over_ground: float,
               itdma_keep_flags: bool,
               itdma_number_of_slots: int,
               itdma_slot_increment: int,
               latitude: float,
               longitude: float,
               navigational_status: int,
               position_accuracy: int,
               raim: int,
               rate_of_turn: float,
               sotdma_spare: str,
               sotdma_slot_number: int,
               sotdma_slot_offset: int,
               sotdma_slot_time_out: int,
               sotdma_utc_hour: int,
               sotdma_utc_minute: int,
               spares: list,
               special_manouvre_indicator: int,
               speed_over_ground: float,
               time_stamp: int,
               true_heading: int,
               ) -> None:


        self.course_over_ground = course_over_ground
        self.itdma_keep_flags = itdma_keep_flags
        self.itdma_number_of_slots = itdma_number_of_slots
        self.itdma_slot_increment = itdma_slot_increment
        self.latitude = latitude
        self.longitude = longitude
        self.navigational_status = navigational_status
        self.position_accuracy = position_accuracy
        self.raim = raim
        self.rate_of_turn = rate_of_turn
        self.sotdma_spare = sotdma_spare
        self.sotdma_slot_number = sotdma_slot_number
        self.sotdma_slot_offset = sotdma_slot_offset
        self.sotdma_slot_time_out = sotdma_slot_time_out
        self.sotdma_utc_hour = sotdma_utc_hour
        self.sotdma_utc_minute = sotdma_utc_minute
        self.spares = spares
        self.special_manouvre_indicator = special_manouvre_indicator
        self.speed_over_ground = speed_over_ground
        self.time_stamp = time_stamp
        self.true_heading = true_heading


