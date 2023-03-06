#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import time
import GVS
import logging 
from Logger import Logger
import random
from functools import wraps

def ReadTemperatureStub(fn):        # wird als Decorator benutzt um künstliche Temperaturwerte 
    @wraps(fn)                      # zum Debuggen ohne Sensoren zu erzeugen
    def wrapper(self):
        self.temperature = round(random.uniform(10.00, 45.00), 2)
        self.SetLastUpdate()
        return True
    return wrapper

@dataclass
class Sensor:
    sensorType: str
    sensorName: str
    sensorAddress:str
    temperature: float
    adjustment: float
    lastUpdate: str
    lastError: str

    @ReadTemperatureStub    # im prod Decorator auskommentieren
    def ReadTemperature(self)->bool: # Aus Systembus Temperatur eines einzelnen Sensors auslesen  
        # Aus Systembus Temperatursensoren DS18B20 auslesen
        line1und2 = self.ReadBus()                          # Liste füllen
        
        line1 = line1und2.pop(0)                       # Liste entladen       
        line2 = line1und2.pop(0)

        # lastUpdate timestamp setzen
        self.SetLastUpdate()

        if 'Fehler' in line1 :                         # Abbruch bei Lesefehler im Systembus
            self.lastError = line1 + line2
            return False
        else :
            # Position von t=..... in der 2. Zeile finden
            temperaturStr = line2.find('t=')           # t=..... finden
            tempData = line2[temperaturStr + 2:]
            # auf 1 Nachkommastelle runden
            tempCelsius   = round(float(tempData) / 1000, 1)
            if tempCelsius <= 0 :
                self.temperature = tempCelsius  # Temperaturwert für Druckprotokoll speichern
                self.lastError = 'Fehler in Sensor.ReadTemperature: Negativen Wert ausgelesen, sollte > 0 sein'
                return False

            # Korrekturwert des Sensors dazu addieren
            self.temperature = round(tempCelsius + self.adjustment, 1)

            return True

    def ReadBus(self)->list:           # Systembus lesen , 2 Zeilen je Sensor
        line1     = ''                 # Initialisierung
        line2     = ''
        line1und2 = [line1, line2]     # beide Zeilen in Liste
        i         = 0
        imax      = 2                  # max Leseversuche / Iterationen
        iwait     = 0.5                # Sekunden warten bei Iteration
            
        # Lesen, ggf. Nachlesen, falls keine Temperatur gefunden
        while 'YES' not in line1 or 't=' not in line2 :
            i = i + 1
            if i > 1 : time.sleep (iwait) # mit Nachlesen warten !

            try :
                f = open(self.sensorAddress, 'r')
            except IOError as ioe:               # Abbruch, da Nachlesen erfolglos
                line1 = 'Fehler in Sensor.ReadBus :' + '\n'
                line1 = str(ioe) + '\n'          # IO Error Beschreibung
                line2 = 20*' ' + 'Index ' + self.sensorAddress + '\n' 
                line2 = line2 + 20*' ' + 'konnte im one-wire bus nicht ausgelesen werden '
                line1und2 = [line1, line2]
                return (line1und2)        # Abbruch , Rückgabe IO Fehler in Liste
            
            line1 = f.readline()          # 1. Zeile lesen
            line2 = f.readline()          # 2. Zeile lesen
            
            line1und2 = [line1, line2]    # Liste erstellen
            
            f.close()
            
            if i > imax :                 # Abbruch , da Nachlesen erfolglos
                line1 = 'Fehler im Skript Func_Sens.Temp.ReadBus'
                line2 = str(imax) + ' Iterationen überschritten' 
                line1und2 = [line1, line2]           
                return (line1und2)        # Abbruch , Rückgabe Fehler in Liste
        
        return (line1und2)                # fehlerfreies Ergebnis als Liste zurück

    def SetLastUpdate(self):
        self.lastUpdate = time.strftime("%Y.%m.%d %H:%M:%S")

############################################ SensorList Class ############################################
def create_sensor_list():  # SensorList default_factory
    sensorList = list()
    # typisierte Sensoren Liste aus GVS sensTab und sensList erzeugen
    for sensorTyp in GVS.SensTypList:
        for t in GVS.SensList:
            if t in GVS.SensTab.keys():
                s = Sensor(sensorType=sensorTyp, sensorName=t, 
                    sensorAddress=GVS.SensTab.get(t), temperature=0.0, adjustment=0.0, lastUpdate='00.00.0000 00:00:00', lastError=None)                       
                sensorList.append(s)
    return sensorList

@dataclass
class SensorList:
# field sorgt dafür das sensorList instanzbezogen initialisiert wird 
# normale default Initialisierungen sind vergleichbar mit statics
    sensorList: list = field(default_factory=create_sensor_list)

    def __iter__(self):
        return iter(self.sensorList)
    def __next__(self):
        return next(self.sensorList)                                                

    def ReadAll(self, Typ: str)->bool:   # aus Systembus alle Temperaturen zu allen Sensoren eines Typs auslesen
                                         # und in GVS.SensTab speichern und Rückgabe zum Druck aufbereiteter Textzeilen
    
        Ergebnis = True

        for sens in self.sensorList:             # Über alle Sensoren iterieren und
            if sens.sensorType != Typ:
                continue                                                                      
            
            # Temperaturwert des einzelnen Sensors auslesen
            # Prüfung , ob ausgelesener Wert fehlerhaft
            
            # GVS.Senstab aus Kompatibilitätsgründen aktualisieren (eigentlich nicht mehr nötig)
            if not sens.ReadTemperature():                    # Fehler beim Auslesen, aus Kompatibiliät wird GVS.SensTab noch aktualisiert
                GVS.SensTab [sens.sensorName + '_Stp'] = sens.lastError
                GVS.SensTab [sens.sensorName + '_Tmp'] = sens.temperature
                Ergebnis = False                             # --> mindestens ein Lesefehler aufgetreten
            else :                                            # NEIN : nicht fehlerhaft ausgelesen
                GVS.SensTab [sens.sensorName + '_Stp'] = sens.lastUpdate
                GVS.SensTab [sens.sensorName + '_Tmp'] = sens.temperature
        
        return Ergebnis  # Rückgabe zum Druck aufbereiteter Textzeilen      

    def PrintResults(self, Typ: str)->None:
        logSensor = Logger().GetLogger("Sensor") # Console/File Ausgaben

        for sens in self.sensorList:             # Über alle Sensoren iterieren und Ergebnisse ausgeben
            Text = ""
            if sens.sensorType != Typ:
                continue 
            if sens.lastError != "":
                Text = Text + ' ' + sens.lastError                          # timestamp = Fehler ...
                Text = Text + ' ' + sens.sensorName                         # Sensor
                Text = Text + ' ' + '\n'                                    # neue Zeile
                Text = Text + 20 * ' ' + sens.temperature                   # einrücken , Temperaturwert
                Text = Text + ' ' + '\n' + 20 * ' '                         # neue Zeile , einrücken
            else:
                # Textzeilen OK fehlerfreie Sensoren aufbereiten
                Text  = Text + ' ' + sens.sensorName                        # Sensor
                Text  = Text + ' ' + sens.temperature + ' '                 # Temperaturwert in gleicher Zeile
            logSensor.log(logging.Info, Text)
