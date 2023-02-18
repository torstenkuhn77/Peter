#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Sensor import Sensor
from Sensor import Sensors

#Sensors wrapped GVS Konfiguration objektorientiert

# Sensors implementiert Iterator protokoll, so kann man ziemlich einfach drüber iterieren 
for s in Sensors():
    print(s.sensorType)
    print(s.sensorName)
    print()

print('ready')
