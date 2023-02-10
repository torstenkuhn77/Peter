#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Sensor import Sensor
from Sensor import Sensors

sens = Sensors()

for s in sens.sensorList:
    print(s)
    print()

print('ready')
