import pathlib
from datetime import datetime, timezone

import tomllib

global AIS

toml_file = pathlib.PurePath(__file__).with_suffix(".toml")

if not pathlib.Path(toml_file).exists():
    raise FileNotFoundError(f"Configuration file {toml_file} not found")

with open(toml_file, "rb") as configs:
    AIS = tomllib.load(configs)

payload_chars = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":")
payload_chars += (";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E")
payload_chars += ("F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P")
payload_chars += ("Q", "R", "S", "T", "U", "V", "W", "`", "a", "b", "c")
payload_chars += ("d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n")
payload_chars += ("o", "p", "q", "r", "s", "t", "u", "v", "w")

PAYLOAD: dict = {}
for v, k in enumerate(payload_chars):
    PAYLOAD[k] = f"{bin(v).lstrip('0b'):0>6}"


def check_the_bits(bits: str, length: int = 0) -> str:
    """Function that checks if the string consists of only bits, zeroes and onses, and
    wether the length is correct. The function accepts strings of bits with and without
    the '0b' prefix
    """
    bits = str(bits)

    if bits.startswith("0b"):
        bits = bits[2:]

    if not all(c in "01" for c in bits):
        raise ValueError(f"Invalid data, got {bits}, expected only 0|1")

    if length > 0 and len(bits) != length:
        raise ValueError(f"Invalid length, got {len(bits)}, expected {length} bits")

    return bits


def bin2dec(bits: str, factor: float = 1, signed: bool = False) -> float:
    """Function that takes in a string representing a binary number and returns
    a decimal number. The can be just zeros and ones, or a binary value that
    starts with '0b', like the output of bin().

    If signed is set to 'True' the first bit is condidered as the sign
    The converted number will be multiplied by 'factor' before it is returned.

    Example:
        def bin2dec(bin(23)) returns 23
        bin2dec(bin(23), factor=10, signed=True) returns -70
    """
    bits = check_the_bits(bits)

    if signed:
        if bits[0] == "1":
            bits = "".join("1" if bit == "0" else "0" for bit in bits)
            return -(int(bits, 2) + 1) * factor
        else:
            return int(bits[1:], 2) * factor
    else:
        return int(bits, 2) * factor


def decode_course_over_ground(cog: str) -> dict:
    cog = check_the_bits(cog, 12)
    cog = bin2dec(cog)

    _cog: dict = {}
    _cog["value"] = cog
    _cog["valid"] = cog <= 3600
    if str(cog) in AIS["courses_over_ground"].keys():
        _cog["state"] = AIS["courses_over_ground"][str(cog)]
    elif cog <= 3600:
        _cog["value"] = cog / 10
        _cog["unit"] = "degrees"

    return _cog


def decode_mmsi(mmsi: str) -> dict:
    _mmsi: dict = {}
    _mmsi["mmsi"] = mmsi

    match mmsi:
        case part if mmsi[0:3] in ("974", "972"):
            _mmsi["transmitter_class"] = AIS["MID_Formats"][part]
            _mmsi["mid"] = None
        case part if mmsi[0:3] in ("970", "111"):
            _mmsi["transmitter_class"] = AIS["MID_Formats"][part]
            _mmsi["mid"] = mmsi[3:6]
        case part if mmsi[0:2] in ("99", "98", "00"):
            _mmsi["transmitter_class"] = AIS["MID_Formats"][part]
            _mmsi["mid"] = mmsi[2:5]
        case part if mmsi[0] in ("8", "0"):
            _mmsi["transmitter_class"] = AIS["MID_Formats"][part]
            _mmsi["mid"] = mmsi[1:4]
        case _:
            _mmsi["transmitter_class"] = AIS["MID_Formats"]["MID"]
            _mmsi["mid"] = mmsi[0:3]

    if _mmsi["mid"] in AIS["MIDs"].keys():
        _mmsi["flag"] = AIS["MIDs"][_mmsi["mid"]]

    return _mmsi


def decode_position(longitude: str, latitude: str) -> dict:
    longitude = check_the_bits(longitude, 28)
    latitude = check_the_bits(latitude, 27)

    longitude: int = int(bin2dec(longitude, signed=True))
    latitude: int = int(bin2dec(latitude, signed=True))
    position: dict = {}

    position["longitude"] = {"state": None}
    if longitude == (181 * 600_000):
        position["longitude"]["state"] = AIS["longitudes"]["181"]
    longitude = longitude / 600_000

    position["longitude"]["value"] = (
        f"{int(abs(longitude)):0>3}* "
        f"{60 * (abs(longitude) - int(abs(longitude))):02.4f}' "
        f"{(AIS['longitudes']['west'] if longitude < 0 else AIS['longitudes']['east'])}"
    )
    position["longitude"]["valid"] = (
        longitude >= -180 and longitude <= 180 or longitude == 181
    )

    position["latitude"] = {"state": None}
    if latitude == (91 * 600_000):
        position["latitude"]["state"] = AIS["latitudes"]["91"]
    latitude = latitude / 600_000

    position["latitude"]["value"] = (
        f"{int(abs(latitude)):0>2}* "
        f"{60 * (abs(latitude) - int(abs(latitude))):02.4f}' "
        f"{(AIS["latitudes"]["south"] if latitude < 0 else AIS["latitudes"]["north"])}"
    )
    position["latitude"]["valid"] = latitude >= -90 and latitude <= 90 or latitude == 91

    position["geopos"] = (longitude, latitude)

    return position


def decode_rate_of_turn(rot: str) -> dict:
    rot = check_the_bits(rot, 8)
    rot = bin2dec(rot, signed=True)

    _rot: dict = {}
    _rot["value"] = rot
    if str(rot) in AIS["rates_of_turn"].keys():
        _rot["description"] = AIS["rates_of_turn"][str(rot)]
    elif rot < 0:
        _rot["description"] = AIS["rates_of_turn"]["TO_PORT"]
        _rot["value"] = -1 * (rot / 4.733) ** 2
    else:
        _rot["description"] = AIS["rates_of_turn"]["TO_STARBOARD"]
        _rot["value"] = (rot / 4.733) ** 2
    _rot["unit"] = "degrees/minute"

    return _rot


def decode_speed_over_ground(sog: str) -> dict:
    sog = check_the_bits(sog, 10)
    sog = bin2dec(sog)

    _sog: dict = {}
    _sog["value"] = sog
    if sog in AIS["speeds_over_ground"].keys():
        _sog["state"] = AIS["speeds_over_ground"][sog]
    else:
        _sog["state"] = "Has speed"
        _sog["value"] = sog / 10
    _sog["unit"] = "knots"

    return _sog


def decode_time_stamp(time_stamp: str) -> dict:
    """UTC second when the report was generated by the electronic position
    system (EPFS) (0-59, or 60 if time stamp is not available, which should
    also be the default value, or 61 if positioning system is in manual
    input mode, or 62 if electronic position fixing system operates in
    estimate"""
    time_stamp = check_the_bits(time_stamp, 6)
    time_stamp = bin2dec(time_stamp)

    _time_stamp: dict = {}
    _time_stamp["value"] = time_stamp
    if str(time_stamp) in AIS["time_stamps"].keys():
        _time_stamp["description"] = AIS["time_stamps"][str(time_stamp)]
    else:
        _ts = datetime.now(timezone.utc).replace(second=time_stamp)
        _time_stamp["description"] = f'{_ts.isoformat('T')}'
    _time_stamp["unit"] = "seconds (UTC)"

    return _time_stamp


def decode_true_heading(th: str) -> dict:
    """Degrees (0-359) (511 indicates not available = default)"""
    th = check_the_bits(th, 9)
    th = bin2dec(th)

    _th: dict = {}
    _th["value"] = th
    if str(th) in AIS["true_headings"].keys():
        _th["valid"] = AIS["true_headings"][str(th)]
    else:
        _th["valid"] = th < 360
    _th["unit"] = "degrees"

    return _th


def payload_to_binary(payload: str) -> str:
    if not all(c in payload_chars for c in payload):
        raise ValueError(f"Invalid data, unsupported character in {payload}")

    _payload: str = ""
    for c in payload:
        _payload += PAYLOAD[c]
    return _payload
