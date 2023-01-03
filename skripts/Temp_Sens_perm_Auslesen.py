#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time , sys
 
# Systempfad zum Sensor, weitere Systempfade könnten über ein Array
# oder weiteren Variablen hier hinzugefügt werden.

# Kesseltemperatur  Sensor 28-030997790a01
sensorKT = '/sys/bus/w1/devices/28-030997790a01/w1_slave'

# Vorlauftemperatur Sensor 28-030997790e32
sensorVT = '/sys/bus/w1/devices/28-030997790e32/w1_slave'

# Raumtemperatur    Sensor 28-0309977914a4
sensorRT = '/sys/bus/w1/devices/28-0309977914a4/w1_slave'

# Boilertemperatur  Sensor 28-0316a27937aa
sensorBT = '/sys/bus/w1/devices/28-0316a27937aa/w1_slave'

# Test              Sensor 28-0316a2793737
sensorTest = '/sys/bus/w1/devices/28-0316a2793737/w1_slave'


def readTempSensor(sensorName) : # Aus Systembus Temperatursensoren DS18B20 auslesen
    f = open(sensorName, 'r')
    lines = f.readlines()
    print ('lines =')
    print (lines)
    print ()
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
        tempCelsius = round((float(tempData) / 1000.0) , 1)
        
        print ('sensorName ',sensorName,' tempCelsius ',tempCelsius )
        print ()
                
        # Rückgabe als Array - [0] tempCelsius => Celsius...
        return [tempCelsius]

print ("ausgelesene Temperatursensoren , Werte in °C")

try:
    while True :
        # Messung mit Timestamp auf Console ausgeben
        KTakt = (readTempLines(sensorKT)[0])
        VTakt = (readTempLines(sensorVT)[0]) + 4 # Korrektur des Meßwertes
        RTakt = (readTempLines(sensorRT)[0]) + 1 # Korrektur des Meßwertes
        BTakt = (readTempLines(sensorBT)[0]) + 3 # Korrektur des Meßwertes
        Test  = (readTempLines(sensorTest)[0]) 
        print("  " ,time.strftime("%d.%m.%Y %H:%M:%S")
              ,"Kessel" , KTakt , "Vorlauf" , VTakt , "Raum" , RTakt,"Boiler",BTakt,"Testsensor",Test)
        
        # nächste Messung nach x Sekunden 
        time.sleep(3)

except KeyboardInterrupt:
    # Programm beendet mit CTRL+C
    print('Temperaturmessung beendet mit CTRL+C oder Strg+C')

except Exception as e:
    print('Fehler beim Auslesen des Sensors ')
    print(str(e))
    sys.exit(1)

finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    print('Funktion Func_Temp_Sens beendet')
    sys.exit(0)
