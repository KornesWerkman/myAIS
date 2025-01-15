# myAIS

myAIS is a pure vanilla python AIS NMEA parser that does not rely on any other packages.

myAis is written against python 3.13 and only uses features of the standard library

## Supported messages and data fields

The following fields are decoded from the payload of the VDO/VDM sentences

|Field                       |Message 1, 2 & 3|Message 4 & 11|Message 5|Message 6|Message 7 & 13|Message 8|Message 9|Message 10|Message 12|Message 14|Message 15|Message 16|Message 17|Message 18|Message 19|Message 20|Message 21|Message 22|Message 23|Message 24|Message 25|Message 26|Message 27|
|----------------------------|:--------------:|:------------:|:-------:|:-------:|:------------:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
|Message ID                  |&check;         |&check;       |&check;  |&check;  |&check;       |&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|
|Repeat Indicator            |&check;         |&check;       |&check;  |&check;  |&check;       |&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|
|User ID                     |&check;         |&check;       |&check;  |&check;  |&check;       |&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|
|Navigational status         |&check;         |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Rate of turn, ROT           |&check;         |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Speed over ground, SOG      |&check;         |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Position accuracy           |&check;         |&check;       |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Longitude                   |&check;         |&check;       |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Latitude                    |&check;         |&check;       |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Course over ground, COG     |&check;         |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|True heading                |&check;         |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Time stamp                  |&check;         |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Special manoeuvre indicators|&check;         |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|Spare                       |&check;         |&check;       |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|RAIM                        |&check;         |&check;       |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|ITDMA                       | 3              |_             |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|SOTDMA                      | 1 & 2          |&check;       |_        |_        |_             |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|

The following additional information can be derived from this info

### Message ID

The following additional info can be decoded out of an MMSI

 - AIS Class Information (A or B)

### User ID

The following additional info can be decoded out of an MMSI

 - Transmitter class
 - MID
 - Flag
