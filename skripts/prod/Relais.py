#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import time
import GVS

@dataclass
class Relais:
    Name: str
    Function: str
    GPIO: int
    PIN: int
    log: bool
    hist: bool
    lastUpdate: str
    lastError: str

    def SetLastUpdate(self):
        self.lastUpdate = time.strftime("%Y.%m.%d %H:%M:%S")

def create_relais_list():  
    relaisList: list = list()
    # typisierte Relais Liste aus GVS RelTab und RelList erzeugen
    for relaisName in GVS.RelList:
        gpio = GVS.RelTab.get(relaisName + "_GPIO")
        pin = GVS.RelTab.get(relaisName + "_PIN")
        funk = GVS.RelTab.get(relaisName + "_Funk")
        log = GVS.RelTab.get(relaisName + "_Log")
        hist = None
        if GVS.RelTab.get(relaisName + "_Hist"):
            hist = GVS.RelTab.get(relaisName + "_Hist")
        r = Relais(Name=relaisName, Function=funk,GPIO = gpio, PIN=pin, log=log, his = hist, 
                    lastUpdate='00.00.0000 00:00:00', lastError=None)                       
        relaisList.append(r)
    return relaisList


@dataclass
class Relais:
# field sorgt dafür das relaisList instanzbezogen initialisiert wird 
# normale default Initialisierungen sind vergleichbar mit statics
    relaisList: list = field(default_factory=create_relais_list)

    def __iter__(self):
        return iter(self.relaisList)
    def __next__(self):
        return next(self.relaisList)                                                
    
