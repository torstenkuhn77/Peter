#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
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

def create_sensor_list():  
    sensorList: list = list()
    # typisierte Sensoren Liste aus GVS sensTab und sensList erzeugen
    for sensorTyp in GVS.SensTypList:
        for t in GVS.SensList:
            if t in GVS.SensTab.keys():
                s = Sensor(sensorType=sensorTyp, sensorName=t, 
                    sensorAddress=GVS.SensTab.get(t), temperature=0.0, adjustment=0.0, lastUpdate='00.00.0000 00:00:00', lastError=None)                       
                sensorList.append(s)
    return sensorList


@dataclass
class Sensors:
# field sorgt dafür das sensorList instanzbezogen initialisiert wird 
# normale default Initialisierungen sind vergleichbar mit statics
    sensorList: list = field(default_factory=create_sensor_list)

    def __iter__(self):
        return iter(self.sensorList)
    def __next__(self):
        return next(self.sensorList)                                                
    
