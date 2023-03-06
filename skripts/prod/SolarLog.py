#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Auslesen von Daten des Solar-Log über JSON Schnittstelle 
# siehe hier : https://constey.de/2014/10/solarlog-200-momentanwerte-per-kommandozeile-auslesen/

import json
from socket import timeout
import urllib.request
from urllib.error import URLError, HTTPError
from dataclasses import dataclass, field
import time
import random
from functools import wraps


#   Beschreibung Solar-Log JSON Schnittstellendaten : ##################
#   100 - LastUpdateTime
#   101 - W Pac (Gesamtleistung) aller Zähler & WR
#   102 - W Pdc (Gestamtleistung aller WR)
#   103 - V Uac Durchschnittliche Spannung UAC der Wechselrichter
#   104 - V Durchschnittliche Spannung UDC der Wechselrichter
#   105 - Wh Durchschnittliche Spannung UDC der Wechselrichter
#   106 - Wh Summierter gestriger Tagesertrag aller Wechselrichter
#   107 - Wh Summiertes Monatsertrag aller WR
#   108 - Wh Summiertes Jahresertrag aller WR
#   109 - Wh Gesamtertrag aller Wechselrichter
#   110 - W momentaner Gesamtverbrauch PAC aller Verbauchszähler
#   111 - Wh Summierter Verbrauch aller Verbauchs-zähler
#   112 - Wh Summierter Verbrauch des gestrigen Tages; alle Verbauchszähler
#   113 - Wh Summierter Verbrauch des Monats; alle Verbauchszähler
#   114 - Wh Summierter Verbrauch des Jahres, alle Verbauchszähler
#   115 - Wh Summierter Gesamtverbrauch, alle Ver-bauchszähler
#   116 - Wp Installierte Generatorleistung

def ReadSolarlogStub(fn):        # wird als Decorator benutzt um künstliche Stromwerte 
    @wraps(fn)                   # zum Debuggen ohne Solaranlage zu simulieren
    def wrapper(self):
        self.Verbrauch = round(random.uniform(1000.00, 4500.00), 2)
        self.Erzeugung = round(random.uniform(500.00, 15000.00), 2)
        self.Bezug = round(random.uniform(1000.00, 2000.00), 2)
        self.SetLastUpdate()
        return True
    return wrapper

@dataclass
class SolarLog:
    ipAddress: str
    Verbrauch: float
    Erzeugung: float
    Bezug: float
    lastUpdate: str
    lastError: str
    Code: int

    def __init__(self, ipAddr: str) -> None:
        self.ipAddress = ipAddr

    @ReadSolarlogStub
    def Read(self)->bool:   # Daten vom Solar-Log einlesen und verarbeiten
        try:                # Update der JSON-Schnittstelle erfolgt alle 15 sec
            self.lastUpdate = time.strftime("%Y.%m.%d %H:%M:%S")
            self.Verbrauch = 0.0
            self.Erzeugung = 0.0
            self.Bezug = 0.0
                        
            req = urllib.request.Request('http://'+ self.ipAddress +'/getjp')
            req.add_header('Content-Type', 'application/json; charset=utf-8')

            data = '{"801" : {"170" : null}}'
            jd = json.dumps(data)
            jb = jd.encode('utf-8')

            req.add_header('Content-Length', len(jb))

            response = urllib.request.urlopen(req, jb)       # Einlesen
            
            self.Code = response.getcode()

            if self.Code != 200:
                self.lastError = "Fehler Solar_Log.Lesen JSON Schnittstelle code : " + self.Code             
            else :
                cb = response.read()
                s = cb.decode('ascii')     
                
                # konvertiert die gelesenen bytes in einen json string
                current = json.loads(s)
                
                lut    = current["801"]["170"]["100"]         # last update des Solar-Log time dd.mm.yy hh.mm.ss
                if lut == "ACCESS DENIED":
                    self.lastError = "Fehler Solar_Log.Lesen JSON Schnittstelle " + lut
                else :
                    day    = lut[0:2] + ' '                   # Konvertierung zum üblichen timestamp
                    month  = lut[3:5] + '.'
    #               year   = lut[6:8]
                    year   = time.strftime("%Y.")
                    Zeit   = lut[9:17]
                    
                    self.lastUpdate = year + month + day + Zeit
                                                                # update globale Variablen in GVS
                    self.Verbrauch = round(current["801"]["170"]["110"]/ 1000 ,2) # 110 siehe oben
                    self.Erzeugung = round(current["801"]["170"]["101"]/ 1000 ,2) # 101 siehe oben
                    self.Bezug     = round((self.Erzeugung - self.Verbrauch), 2)

            return (True)
        # Error - handling ################################################################
        except ConnectionResetError:
            self.lastError = 'Fehler Solar_Log.Lesen ConnectionResetError'
        except timeout: 
            self.lastError = 'Fehler Solar_Log.Lesen Timeout'
        except HTTPError as e:
            # keine HTTP-Verbindung zum Solar-Log
            self.lastError = 'Fehler Solar_Log.Lesen HTTP-Verbindung HTTPError' + '\n' 
            self.lastError = self.lastError + 20 * ' ' + str(e.code)         # 20 Stellen einrücken , neue Zeile
        except URLError as e:
            # keine LAN-Verbindung zum Solar-Log
            self.lastError = 'Fehler Solar_Log.Lesen LAN-Verbindung URLError' + '\n' 
            self.lastError = self.lastError + 20 * ' ' + str(e.reason)              # 20 Stellen einrücken , neue Zeile
        
        return (False)
        
