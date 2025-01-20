import pathlib

import tomllib

global NMEA

toml_file = pathlib.PurePath(__file__).with_suffix(".toml")

if not pathlib.Path(toml_file).exists():
    raise FileNotFoundError(f"Configuration file {toml_file} not found")

with open(toml_file, "rb") as configs:
    NMEA = tomllib.load(configs)


def calculate_check_sum(data: str, checksum: str) -> dict:
    data = data[1:]
    check_sum: dict = {}
    check_sum["value"] = checksum
    cchecksum = 0

    for c in data:
        cchecksum ^= ord(c)
    check_sum["calculated"] = (
        f"{cchecksum:X}"  # TODO this does not work yet for single digit checksums (<= 'A')
    )
    check_sum["valid"] = check_sum["value"] == check_sum["calculated"]

    return check_sum
