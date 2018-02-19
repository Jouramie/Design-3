#!/usr/bin/env bash

device="video1"
table="5"


# save for further
#uvcdynctrl -d $device -W /home/genou/dev/station/calibration/camera_state$table

# later will load we
uvcdynctrl -d $device -L /home/genou/dev/station/calibration/camera_state$table

uvcdynctrl -d $device -s 'Brightness' 0

python3 /home/genou/dev/station/src/scripts/calibration_script.py 15


