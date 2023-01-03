# script name : /home/pi/skripts/prod/Func_Sensor.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time

# Systempfad zum Sensor, weitere Systempfade könnten über ein Array
# oder weitere Variablen hier hinzugefügt werden.

# Kesseltemperatur  Sensor 28-030997790a01
sensorKT = '/sys/bus/w1/devices/28-030997790a01/w1_slave'

# Vorlauftemperatur Sensor 28-030997790e32
sensorVT = '/sys/bus/w1/devices/28-030997790e32/w1_slave'

# Raumtemperatur    Sensor 28-0309977914a4
sensorRT = '/sys/bus/w1/devices/28-0309977914a4/w1_slave'

# Boilertemperatur  Sensor 28-0316a27937aa
sensorBT = '/sys/bus/w1/devices/28-0316a27937aa/w1_slave'

 
# def readTempSensor(sensorName) : # Aus Systembus Temperatursensoren DS18B20 auslesen
#     f = open(sensorName, 'r')
#     lines = f.readlines()
#     f.close()
#     return lines
#  
# def readTempLines(sensorName) :   # Tabelle erstellen : sensorName , Temperaturwert
#     lines = readTempSensor(sensorName)
# 
#     # für Testzwecke :
#     print (sensorName)
#     print (lines)
#     print ()
# 
#     # Solange nicht die Daten gelesen werden konnten , Endlosschleife
#     while lines[0].strip()[-3:] != 'YES':
#         time.sleep(0.2)
#         lines = readTempSensor(sensorName)
#     temperaturStr = lines[1].find('t=')
#     # überprüfen , ob die Temperatur gefunden wurde.
#     if temperaturStr != -1 :
#         tempData = lines[1][temperaturStr+2:]
#         tempCelsius = float(tempData) / 1000
#         if sensorName == sensorVT :
#             tempCelsius = tempCelsius + 4.1  # Korrektur des Meßwertes  Vorlauf
#         if sensorName == sensorRT :
#             tempCelsius = tempCelsius + 1.8  # Korrektur des Meßwertes  Raum
#         if sensorName == sensorBT :
#             tempCelsius = tempCelsius + 4.1  # Korrektur des Meßwertes  Boiler
#         # Rückgabe als Array - [0] tempCelsius => Celsius... 
#         return [round(tempCelsius,1)]       # auf 1 Nachkommastelle gerundet
#     
#     return (sensorKT,sensorVT,sensorRT,sensorBT,readTempLines)
#     
# # für Testzwecke :
# print ()
# print (readTempSensor)
# print ('ausgelesene Temperatursensoren :')
# readTempLines
# KTakt  =   readTempLines(sensorKT)[0]
# VTakt  =   readTempLines(sensorVT)[0]
# RTakt  =   readTempLines(sensorRT)[0]
# BTakt  =   readTempLines(sensorBT)[0]
# print  ('Kessel ',KTakt,' Vorlauf ',VTakt,' Wohnraum ',RTakt,' Boiler ',BTakt)

##########  n e u  ######################################
# sens = sensorKT
# def Temp(sens) : # Aus Systembus Temperatursensoren DS18B20 auslesen
#     f = open(sens, 'r')
#     line = f.readline()
#     f.close()
#     # für Testzwecke :
#     print (sens)
#     print (line)
#     print ()
#     return()

# shell befehl : cat /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
# Ergebnis :
# pi@PB-raspberrypi:~ $ cat /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
# 92 02 55 05 7f a5 a5 66 75 : crc=75 YES
# 92 02 55 05 7f a5 a5 66 75 t=41125
# pi@PB-raspberrypi:~ $ 

sensorKT = '/sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave'
f = open(sensorKT, 'r')
line = f.readline()
f.close()
temperaturStr = line.find('t=')
# für Testzwecke :
print (sensorKT)
print (line)
print (temperaturStr)
print ()

# Ergebnis :
# /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
# 95 02 55 05 7f a5 a5 66 a5 : crc=a5 YES
# 
# -1
