import json
from datetime import datetime, timezone

import ais
import nmea


def find_value_in_dictionary(value: (int, str), dictionary: dict) -> dict:
    _dictionary: dict = {}
    _dictionary["value"] = value
    _dictionary["description"] = dictionary[str(value)]
    return _dictionary


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


def decode_ais(binary: str) -> dict:
    decoded_ais: dict = {}

    decoded_ais["message_id"] = find_value_in_dictionary(
        int(binary[0:6], 2), ais.AIS["message_ids"]
    )

    decoded_ais["repeat_indicator"] = find_value_in_dictionary(
        int(binary[6:8], 2), ais.AIS["repeat_indicators"]
    )

    decoded_ais["user_id"] = ais.decode_mmsi(f"{int(binary[8:38], 2):0>9}")

    decoded_ais["navigational_status"] = find_value_in_dictionary(
        int(binary[38:42], 2), ais.AIS["navigational_statusses"]
    )

    decoded_ais["rate_of_turn"] = ais.decode_rate_of_turn(binary[42:50])
    decoded_ais["speed_over_ground"] = ais.decode_speed_over_ground(binary[50:60])

    decoded_ais["position_accuracy"] = find_value_in_dictionary(
        int(binary[60:61]), ais.AIS["position_accuracies"]
    )

    decoded_ais["position"] = ais.decode_position(binary[61:89], binary[89:116])
    decoded_ais["course_over_ground"] = ais.decode_course_over_ground(binary[116:128])
    decoded_ais["true_heading"] = ais.decode_true_heading(binary[128:137])
    decoded_ais["time_stamp"] = ais.decode_time_stamp(binary[137:143])

    decoded_ais["special_manoeuvre_indicators"] = find_value_in_dictionary(
        int(binary[143:145], 2), ais.AIS["special_manoeuvre_indicators"]
    )

    decoded_ais["spares"] = {
        "value": binary[145:148],
        "valid": (all(c in "0" for c in binary[145:148])),
    }

    decoded_ais["raim"] = find_value_in_dictionary(
        int(binary[148:149]), ais.AIS["RAIMs"]
    )

    # SOTDMA / ITDMA communication states
    decoded_ais["sync_state"] = find_value_in_dictionary(
        int(binary[149:151], 2), ais.AIS["sync_states"]
    )

    match decoded_ais["message_id"]["value"]:
        case _ if decoded_ais["message_id"]["value"] in (1, 2):
            # SOTDMA
            decoded_ais["slot_time_out"] = find_value_in_dictionary(
                int(binary[151:154], 2), ais.AIS["slot_time_outs"]
            )
            match decoded_ais["slot_time_out"]["value"]:
                case _ if decoded_ais["slot_time_out"]["value"] in (3, 5, 7):
                    # TODO is slot_time_out correct here ??
                    decoded_ais["slot_time_out"] = int(binary[154:], 2)
                case _ if decoded_ais["slot_time_out"]["value"] in (2, 4, 6):
                    decoded_ais["slot_number"] = {"value": int(binary[154:], 2)}
                    decoded_ais["slot_number"]["valid"] = (
                        decoded_ais["slot_number"]["value"] <= 2249
                    )
                case 1:
                    decoded_ais["utc_hour"] = {"value": int(binary[154:159], 2)}
                    decoded_ais["utc_hour"]["valid"] = (
                        decoded_ais["utc_hour"]["value"] <= 23
                    )
                    decoded_ais["utc_minute"] = {"value": int(binary[159:166], 2)}
                    decoded_ais["utc_minute"]["valid"] = (
                        decoded_ais["utc_minute"]["value"] <= 59
                    )
                    decoded_ais["sotdma_spare"] = {"value": binary[166:]}
                    decoded_ais["sotdma_spare"]["valid"] = all(
                        c in "0" for c in binary[166:]
                    )
                case 0:
                    decoded_ais["slot_offset"] = int(binary[154:], 2)

        case 3:
            # ITDMA
            decoded_ais["slot_increment"] = int(binary[151:164], 2)
            decoded_ais["number_of_slots"] = find_value_in_dictionary(
                int(binary[164:167], 2), ais.AIS["number_of_slots"]
            )
            decoded_ais["keep_flag"] = find_value_in_dictionary(
                binary[167:], ais.AIS["keep_flags"]
            )

    return decoded_ais


def decode_sentence(sentence: str) -> dict:
    ts_received = datetime.now(timezone.utc)

    data, check_sum = sentence.split("*")
    fields: dict = split_nmea(data, check_sum)
    fields["delimiter"] = find_value_in_dictionary(
        fields["delimiter"], nmea.NMEA["delimiters"]
    )
    fields["talker_id"] = find_value_in_dictionary(
        fields["talker_id"], nmea.NMEA["talker_ids"]
    )
    fields["sentence_formatter"] = find_value_in_dictionary(
        fields["sentence_formatter"], nmea.NMEA["sentence_formatters"]
    )
    fields["ais_channel"] = find_value_in_dictionary(
        fields["ais_channel"], nmea.NMEA["ais_channels"]
    )
    fields["payload"] = {"value": fields["payload"]}
    fields["payload"]["binary"] = ais.payload_to_binary(fields["payload"]["value"])
    fields["payload"]["length"] = len(fields["payload"]["binary"])
    fields["check_sum"] = nmea.calculate_check_sum(data, check_sum)
    fields["ts_received"] = f'{ts_received.isoformat('T')}'

    decoded_ais = decode_ais(fields["payload"]["binary"])
    return fields, decoded_ais


if __name__ == "__main__":
    # print(ais.AIS)
    # print(nmea.NMEA)
    print(
        json.dumps(
            decode_sentence("!AIVDM,1,1,,A,13u?etPv2;0n:dDPwUM1U1Cb069D,0*23"), indent=2
        )
    )
