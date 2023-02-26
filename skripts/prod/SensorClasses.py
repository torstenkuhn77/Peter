#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import time
import GVS

@dataclass
class Sensor:
    sensorType: str
    sensorName: str
    sensorAddress:str
    temperature: float
    adjustment: float
    lastUpdate: str
    lastError: str

    def ReadTemperature(self)->bool: # Aus Systembus Temperatur eines einzelnen Sensors auslesen  
        # Aus Systembus Temperatursensoren DS18B20 auslesen
        line1und2 = ReadBus()                          # Liste füllen
        
        line1 = line1und2.pop(0)                       # Liste entladen       
        line2 = line1und2.pop(0)

        # lastUpdate timestamp setzen
        self.SetLastUpdate();

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

    def ReadAll(self, Typ: str) -> str:  # aus Systembus alle Temperaturen zu allen Sensoren eines Typs auslesen
                                         # und in GVS.SensTab speichern und Rückgabe zum Druck aufbereiteter Textzeilen
        
        for sens in self.sensorList:             # Über alle Sensoren iterieren und
            if sens.SensorType != Typ:
                continue                                                                      
            
            fErgebnis = sens.ReadTemperature()   # Temperaturwert des einzelnen Sensors auslesen
                                                 # Prüfung , ob ausgelesener Wert fehlerhaft
            
            # GVS.Senstab aus Kompatibilitätsgründen aktualisieren (eigentlich nicht mehr nötig)
            if fErgebnis == False: # Fehler beim Auslesen, aus Kompatibiliät wird GVS.SensTab noch aktualisiert
                GVS.SensTab [sens.sensorName + '_Stp'] = sens.LastError
                GVS.SensTab [sens.Sensorname + '_Tmp'] = sens.temperature
                Lesefehler = True               # --> mindestens ein Lesefehler aufgetreten
                # Textzeilen NOK fehlerhafte Sensoren aufbereiten
                TextNOK = TextNOK + ' ' + sens.LastError                          # timestamp = Fehler ...
                TextNOK = TextNOK + ' ' + sens.sensorName                         # Sensor
                TextNOK = TextNOK + ' ' + '\n'                                    # neue Zeile
                TextNOK = TextNOK + 20 * ' ' + sens.temperature                   # einrücken , Temperaturwert
                TextNOK = TextNOK + ' ' + '\n' + 20 * ' '                         # neue Zeile , einrücken
            else :                                            # NEIN : nicht fehlerhaft ausgelesen
                GVS.SensTab [sens.Sensorname + '_Stp'] = sens.LastUpdate
                GVS.SensTab [sens.Sensorname + '_Tmp'] = sens.temperature
                # Textzeilen OK fehlerfreie Sensoren aufbereiten
                TextOK  = TextOK + ' ' + sens.sensorName        # Sensor
                TextOK  = TextOK + ' ' + sens.temperature + ' ' # Temperaturwert in gleicher Zeile
                    
            if Lesefehler :                                     # ist mindestens ein Lesefehler aufgetreten ?
                Text = Text + 'beim Auslesen der Sensoren ' + Typ + ' ist mindestens ein Fehler aufgetreten :' + '\n'
                Text = Text + 19 * ' ' + TextOK + '\n' + 20 * ' ' + TextNOK
            else :                                              # kein Lesefehler aufgetreten
                Text = Text + time.strftime("%Y.%m.%d %H:%M:%S")
                Text = Text + ' Temperatur aller Sensoren ' + Typ + ' gespeichert in GVS.SensTab :' + '\n'
                Text = Text + 19 * ' ' + TextOK
        
        return (Text)  # Rückgabe zum Druck aufbereiteter Textzeilen      
        # Ende aus Systembus alle Temperatursensoren eines Typs auslesen und in GVS.SensTab speichern   
