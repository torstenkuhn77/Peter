# Programm zum Ein-/Aus-Schalten , Set/Reset des Relais abc mit GPIO Nummer xy
# Ausgabe auf Konsole und in Logdatei

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import GVS            # Zwischenspeicher eigene globale Variablen
from Relais import Relais

def create_relais_list():  
    relaisList = list()
    # typisierte Relais Liste aus GVS RelTab und RelList erzeugen
    for relaisName in GVS.RelList:
        gpio = GVS.RelTab.get(relaisName + "_GPIO")
        pin = GVS.RelTab.get(relaisName + "_PIN")
        funk = GVS.RelTab.get(relaisName + "_Funk")
        log = GVS.RelTab.get(relaisName + "_Log")
        hist = None
        if GVS.RelTab.get(relaisName + "_Hist"):
            hist = GVS.RelTab.get(relaisName + "_Hist")
        r = Relais()
        r.Name = relaisName
        r.Function=funk
        r.GPIO = gpio
        r.PIN=pin
        r.log=log
        r.hist = hist
        r.lastUpdate='00.00.0000 00:00:00'
        r.lastError=None                       
        relaisList.append(r)
    return relaisList

@dataclass
class RelaisList:
# field sorgt dafür das relaisList instanzbezogen initialisiert wird 
# normale default Initialisierungen sind vergleichbar mit statics
    relaisList: list = field(default_factory=create_relais_list)

    def __iter__(self):
        return iter(self.relaisList)
    def __next__(self):
        return next(self.relaisList)                                                

    def findRelais(self, relaisName: str) -> Relais:
        for elem in self.relaisList:
            if elem.Name == relaisName:
                return elem    
        return None

    def ResetAll(self, switch, drucken, loggen) -> None:
        for elem in self.relaisList:
            elem.Reset(switch, drucken, loggen)