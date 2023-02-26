# Programm zum Ein-/Aus-Schalten , Set/Reset des Relais abc mit GPIO Nummer xy
# Ausgabe auf Konsole und in Logdatei

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import time
import RPi.GPIO as GPIO
import GVS            # Zwischenspeicher eigene globale Variablen
import logging 
from Logger import Logger

GPIO.setmode(GPIO.BCM) #  GPIO statt Board Nummern (PINs)

@dataclass
class Relais:
    name: str
    function: str
    gpio: int
    pin: int
    log: bool
    hist: bool
    lastUpdate: str
    lastError: str

    logRelais: Logger

    def __init__(self):
        self.logRelais = Logger().GetLogger("Relais") # Console/File Ausgaben

    # Relais Ein- / Aus-Schalten  Set
    def Set(self, switch: bool, drucken: bool, useRelaisLog: bool): # Relais Ein- / Aus-Schalten  Set
        # zum Relais aus GVS.RelTab GPIO , Funktionsbezeichnung , LogSchalter lesen

        loggen = True

        if useRelaisLog:
            loggen = self.log
        
        if switch : Schalter = 'ein'
        else      : Schalter = 'aus' 

        SetText = ""
        LogText = ""

        # keine Fehler festgestellt -->  vorherigen Zustand prüfen , ggf. Schaltvorgang ausführen , loggen
        GPIO.setwarnings(False)            # Warning vorübergehend abschalten
        GPIO.setup(self.gpio, GPIO.OUT)    # GPIO Modus zuweisen
        GPIO.setwarnings(True)             # Warning wieder einschalten
        
        # To test the value of pin with input method , Returns 0 if OFF=HIGH or 1 if ON=LOW 
        if GPIO.input(self.gpio) : vorher = "aus"
        else                     : vorher = "ein"
        
        if Schalter == 'ein':
            if vorher == 'ein' :                        # Relais bleibt unverändert eingeschaltet
                loggen = False                          # --> kein Log schreiben
                SetText = SetText + self.function + self.name + ' GPIO ' + str(self.gpio) + ' unverändert eingeschaltet '
            else :
                GPIO.output(self.gpio, GPIO.LOW)      # Relais wird eingeschaltet
                time.sleep(1) 
                LogText = self.function + self.name + ' GPIO ' + str(self.gpio) +           ' eingeschaltet             ' 
                SetText = LogText
                
        if Schalter == 'aus':
            if vorher == 'aus' :                        # Relais bleibt unverändert ausgeschaltet
                loggen = False                          # --> kein Log schreiben
                SetText = SetText + self.function + self.name + ' GPIO ' + str(self.gpio) + ' unverändert ausgeschaltet '
            else :
                GPIO.output(self.gpio, GPIO.HIGH)     # Relais wird ausgeschaltet
                time.sleep(1) 
                LogText = self.function + self.name + ' GPIO ' + str(self.gpio) +            ' ausgeschaltet             '
                SetText = LogText
        
        if loggen:                                      # Protokollzeile in Logdatei für Relaissteuerung aus GVS anfügen
            self.logRelais.log(logging.INFO, LogText)
        
        if drucken:                                     # Ausgabe auf Konsole
            self.logRelais.log(logging.INFO, SetText)

    def SetLastUpdate(self):
        self.lastUpdate = time.strftime("%Y.%m.%d %H:%M:%S")
