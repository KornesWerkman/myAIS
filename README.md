# myAIS

myAIS is a pure vanilla python AIS NMEA parser that does not rely on any other packages.

myAis is written against python 3.13 and only uses features of the standard library

## Supported messages and data fields

|Field|Message 1, 2 & 3|Message 4 & 11|Message 5|Message 6|Message 7 & 13|Message 8|Message 9|Message 10|Message 12|Message 14|Message 15|Message 16|Message 17|Message 18|Message 19|Message 20|Message 21|Message 22|Message 23|Message 24|Message 25|Message 26|Message 27|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Message ID|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|
|Repeat Indicator|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|
|User ID|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|&check;|
|navigational_status|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|rate_of_turn|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|speed_over_ground|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|position_accuracy|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|longitude|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|latitude|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|course_over_ground|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|true_heading|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|time_stamp|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|special_manoeuvre_indicators|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|spare|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|RAIM|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
|sotdma|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
