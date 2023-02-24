# shell : python3 /home/pi/skripts/Func_Relais.py

# Programm zum Ein-/Aus-Schalten , Set/Reset des Relais abc mit GPIO Nummer xy
# Ausgabe auf Konsole und in Logdatei

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time , RPi.GPIO as GPIO
import GVS            # Zwischenspeicher eigene globale Variablen
import logging 
from Logger import Logger
from Relais import Relais
from RelaisList import RelaisList

logRelais = Logger().GetLogger("Relais") # Console/File Ausgaben

GPIO.setmode(GPIO.BCM) #  GPIO statt Board Nummern (PINs)

# Relais Ein- / Aus-Schalten  Set
def Set(relaisList: RelaisList, relaisName: str, switch: bool, drucken: bool, loggen: str):    # Relais Ein- / Aus-Schalten  Set
    # zum Relais aus GVS.RelTab GPIO , Funktionsbezeichnung , LogSchalter lesen

    relais = findRelais(relaisList, relaisName)

    if (relais == None):
        logRelais.log(logging.ERROR, "Relais " + relaisName + " not found!")
        return

    RELAIS_GPIO = relais.GPIO
    RELAIS_Bez  = relais.Function

    if loggen == 'RelTab' :
        loggen = relais.log
    
    if switch : Schalter = 'ein'
    else      : Schalter = 'aus' 

    SetText = ""
    LogText = ""

    # keine Fehler festgestellt -->  vorherigen Zustand prüfen , ggf. Schaltvorgang ausführen , loggen

    GPIO.setwarnings(False)            # Warning vorübergehend abschalten
    GPIO.setup(RELAIS_GPIO, GPIO.OUT)  # GPIO Modus zuweisen
    GPIO.setwarnings(True)             # Warning wieder einschalten
    
    # To test the value of pin with input method , Returns 0 if OFF=HIGH or 1 if ON=LOW 
    if GPIO.input(RELAIS_GPIO) : vorher = "aus"
    else                       : vorher = "ein"
    
    if Schalter == 'ein':
        if vorher == 'ein' :                        # Relais bleibt unverändert eingeschaltet
            loggen = False                          # --> kein Log schreiben
            SetText = SetText + RELAIS_Bez + relais.Name + ' GPIO ' + str(RELAIS_GPIO) + ' unverändert eingeschaltet '
        else :
            GPIO.output(RELAIS_GPIO, GPIO.LOW)      # Relais wird eingeschaltet
            LogText = RELAIS_Bez + relais.Name + ' GPIO ' + str(RELAIS_GPIO) +           ' eingeschaltet             ' 
            SetText = LogText
            
    if Schalter == 'aus':
        if vorher == 'aus' :                        # Relais bleibt unverändert ausgeschaltet
            loggen = False                          # --> kein Log schreiben
            SetText = SetText + RELAIS_Bez + relais.Name + ' GPIO ' + str(RELAIS_GPIO) + ' unverändert ausgeschaltet '
        else :
            GPIO.output(RELAIS_GPIO, GPIO.HIGH)     # Relais wird ausgeschaltet
            LogText = RELAIS_Bez + relais.Name + ' GPIO ' + str(RELAIS_GPIO) +           ' ausgeschaltet             '
            SetText = LogText
    
    if loggen:                                      # Protokollzeile in Logdatei für Relaissteuerung aus GVS anfügen
        logRelais.log(logging.Info, LogText)
    
    if drucken:                                     # Ausgabe auf Konsole
        logRelais.log(logging.Info, SetText)

def Reset(relaisList: RelaisList, RELAIS: str , switch: bool, drucken: bool , loggen: str) :       # Relais initialisieren / Reset
    wait = 0.5
    if RELAIS == 'alle' :                             # alle aus RelList
        for relais in relaisList:
            Set(relaisList, relais.Name, switch, drucken, loggen)
            time.sleep(wait)
    else :                                            # ein Einzelnes explizit
        Set(relaisList, RELAIS, switch, drucken, loggen)
        time.sleep(wait)

def findRelais(relaisName: str, relaisList: RelaisList) -> Relais:
    for elem in relaisList:
        if elem.Name == relaisName:
            return elem    
    return None