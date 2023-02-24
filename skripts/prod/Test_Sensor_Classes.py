#!/usr/bin/python3
# -*- coding: utf-8 -*-

from SensorClasses import Sensor
from SensorClasses import Sensors

#Sensors wrapped GVS Konfiguration as a class

# Sensors implements iterator protocol, easier to enumerate 
for s in Sensors():
    print(s.sensorType)
    print(s.sensorName)
    print()

print('ready')
