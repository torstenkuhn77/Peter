#!/usr/bin/python3
# -*- coding: utf-8 -*-

from SensorClasses import Sensor
from SensorClasses import SensorList

#Sensor wrapped GVS Konfiguration as a class

# SensorList implements iterator protocol, easier to enumerate 
for s in SensorList():
    print(s.sensorType)
    print(s.sensorName)

    s.ReadTemperature()

    print(s.temperature)

print('ready')
