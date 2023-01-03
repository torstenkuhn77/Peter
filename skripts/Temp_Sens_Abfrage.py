# script name : /home/pi/skripts/prod/Temp_Sens_Abfrage.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import sys

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

def readTempSensor(sensorName) : # Aus Systembus Temperatursensoren DS18B20 auslesen
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def readTempLines(sensorName) :   # Tabelle erstellen : sensorName , Temperaturwert
    lines = readTempSensor(sensorName)
    # Solange nicht die Daten gelesen werden konnten , Endlosschleife
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')
    # überprüfen , ob die Temperatur gefunden wurde.
    if temperaturStr != -1 :
        tempData = lines[1][temperaturStr+2:]
        tempCelsius = float(tempData) / 1000
        if sensorName == sensorVT :
            tempCelsius = tempCelsius + 4.1 # Korrektur des Meßwertes  Vorlauf
        if sensorName == sensorRT :
            tempCelsius = tempCelsius + 2.2 # Korrektur des Meßwertes  Raum
        if sensorName == sensorBT :
            tempCelsius = tempCelsius + 6.4 # Korrektur des Meßwertes  Boiler
        # Rückgabe als Array - [0] tempCelsius => Celsius... 
        return [round(tempCelsius,1)]       # auf 1 Nachkommastelle gerundet
    
    return (sensorKT,sensorVT,sensorRT,sensorBT,readTempLines)

        

        
        