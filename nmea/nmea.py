import pathlib

import tomllib

global NMEA

toml_file = pathlib.PurePath(__file__).with_suffix(".toml")

if not pathlib.Path(toml_file).exists():
    raise FileNotFoundError(f"Configuration file {toml_file} not found")

with open(toml_file, "rb") as configs:
    NMEA = tomllib.load(configs)


def find_value_in_dictionary(value: (int, str), dictionary: dict) -> dict:
    _dictionary: dict = {}
    try:
        _dictionary["value"] = value
        _dictionary["description"] = dictionary[str(value)]
    except KeyError:
        _dictionary["value"] = value
        _dictionary["description"] = dictionary["others"]

    return _dictionary


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

def split_nmea(data: str, check_sum: str) -> dict:
    fields: dict = {}

    _fields = data.split(",")
    fields["delimiter"] = _fields[0][0]
    fields["talker_id"] = _fields[0][1:3]
    fields["sentence_formatter"] = _fields[0][3:]
    fields["count_of_fragments"] = int(_fields[1])
    fields["fragment_number"] = int(_fields[2])
    fields["sequential_message_id"] = _fields[3]
    fields["ais_channel"] = _fields[4]
    fields["payload"] = _fields[5]
    fields["number_of_fill_bits"] = int(_fields[6])
    fields["check_sum"] = "0x" + check_sum

    return fields


def decode_nmea(sentence: str) -> dict:
    data, check_sum = sentence.split("*")
    fields: dict = split_nmea(data, check_sum)
    fields["delimiter"] = find_value_in_dictionary(
        fields["delimiter"], NMEA["delimiters"]
    )
    fields["talker_id"] = find_value_in_dictionary(
        fields["talker_id"], NMEA["talker_ids"]
    )
    fields["sentence_formatter"] = find_value_in_dictionary(
        fields["sentence_formatter"], NMEA["sentence_formatters"]
    )
    fields["ais_channel"] = find_value_in_dictionary(
        fields["ais_channel"], NMEA["ais_channels"]
    )
    fields["check_sum"] = calculate_check_sum(data, check_sum)

    return fields
