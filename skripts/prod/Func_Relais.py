# shell : python3 /home/pi/skripts/Func_Relais.py

# die Farbsteuerung funktioniert nur bei Ausführung aus der Konsole !
# Beschreibung : https://pypi.org/project/colorama/

# Programm zum Ein-/Aus-Schalten , Set/Reset des Relais abc mit GPIO Nummer xy
# Ausgabe auf Konsole und in Logdatei

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time , RPi.GPIO as GPIO

import GVS            # Zwischenspeicher eigene globale Variablen

import Func_LogDatei  # eigene Funktion Logdatei schreiben

from colorama import init , Fore , Back , Style
                    # init(autoreset=True) Farbe gilt nur je Printposition
                    # init()               Farbe gilt bis Programmende
                    #Farben :
                    #Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Style: DIM, NORMAL, BRIGHT, RESET_ALL

init(autoreset=True)

GPIO.setmode(GPIO.BCM) #  GPIO statt Board Nummern (PINs)

# def Schaltung (RELAIS , switch , drucken , loggen) :    # Relais Ein- / Aus-Schalten  Set
def Set (RELAIS , switch , drucken , loggen) :    # Relais Ein- / Aus-Schalten  Set
    # zum Relais aus GVS.RelTab GPIO , Funktionsbezeichnung , LogSchalter lesen   
    RELAIS_GPIO = GVS.RelTab.get (RELAIS)
    RELAIS_Funk = RELAIS + '_Funk'
    RELAIS_Bez  = GVS.RelTab.get (RELAIS_Funk)

    if loggen  == 'RelTab' :
        loggen  = GVS.RelTab.get (RELAIS + '_Log')
    
    if switch : Schalter = 'ein'
    else      : Schalter = 'aus' 
    
    SetText   =  ''
    LogText   =  ''
       
    # Prüfen , ob Relais / GPIO / Funktionsbezeichnung , LogSchalter korrekt
    if RELAIS   not in GVS.RelTab.keys() :
        LogText   = "Fehler : Relais " + RELAIS + ' nicht in GVS Relais-Tabelle '
        SetText   = Fore.RED + Style.BRIGHT + LogText
        
    else :
        if RELAIS_Funk not in GVS.RelTab.keys() :
            LogText   = "Fehler : Funktionsbezeichnung zu Relais " + RELAIS + ' nicht in GVS Relais-Tabelle '
            SetText   = Fore.RED + Style.BRIGHT + LogText 
        
    # prüfen ob alle Schalter korrekt gesetzt sind

    if switch not in [True , False] :
        if LogText   == '' :
            LogText = 'Fehler : ungültiger Schalter für Relais , nur True=ein oder False=aus zulässig !'
            SetText = Fore.RED + Style.BRIGHT + LogText
        else :
            LogText = LogText + ' und ungültiger Schalter für Relais , nur True=ein oder False=aus zulässig !'
            SetText = Fore.RED + Style.BRIGHT + LogText
    
    if drucken not in [True , False] :
        if LogText   == '' :
            LogText = 'Fehler : ungültiger Schalter für Drucken , nur True=ein oder False=aus zulässig !'
            SetText = Fore.RED + Style.BRIGHT + LogText
        else :
            LogText = LogText + ' und ungültiger Schalter für Drucken , nur True=ein oder False=aus zulässig !'
            SetText = Fore.RED + Style.BRIGHT + LogText
     
    if loggen not in [True , False] :
        if LogText   == '' :
            LogText = 'Fehler : ungültiger Schalter für Loggen , nur True=ein oder False=aus zulässig !'
            SetText = Fore.RED + Style.BRIGHT + LogText
        else :
            LogText = LogText + ' und ungültiger Schalter für Loggen , nur True=ein oder False=aus zulässig !'
            SetText = Fore.RED + Style.BRIGHT + LogText
     
            
    # keine Fehler festgestellt -->  vorherigen Zustand prüfen , ggf. Schaltvorgang ausführen , loggen
    if LogText == '' :
        
        GPIO.setwarnings(False)            # Warning vorübergehend abschalten
        GPIO.setup(RELAIS_GPIO,GPIO.OUT)   # GPIO Modus zuweisen
        GPIO.setwarnings(True)             # Warning wieder einschalten
        
        # To test the value of pin with input method , Returns 0 if OFF=HIGH or 1 if ON=LOW 
        if GPIO.input(RELAIS_GPIO) : vorher = "aus"
        else                       : vorher = "ein"
        
        if Schalter == 'ein':
            if vorher == 'ein' :                        # Relais bleibt unverändert eingeschaltet
                loggen = False                          # --> kein Log schreiben
                SetText = Fore.WHITE + Back.GREEN
                SetText = SetText + RELAIS_Bez + RELAIS + ' GPIO ' + str(RELAIS_GPIO) + ' unverändert eingeschaltet '
            else :
                GPIO.output(RELAIS_GPIO, GPIO.LOW)      # Relais wird eingeschaltet
                LogText = RELAIS_Bez + RELAIS + ' GPIO ' + str(RELAIS_GPIO) +             ' eingeschaltet             ' 
                SetText = Fore.BLACK + Back.GREEN + LogText
                
        if Schalter == 'aus':
            if vorher == 'aus' :                        # Relais bleibt unverändert ausgeschaltet
                loggen = False                          # --> kein Log schreiben
                SetText = Fore.WHITE + Back.RED
                SetText = SetText + RELAIS_Bez + RELAIS + ' GPIO ' + str(RELAIS_GPIO) + ' unverändert ausgeschaltet '
            else :
                GPIO.output(RELAIS_GPIO, GPIO.HIGH)     # Relais wird ausgeschaltet
                LogText = RELAIS_Bez + RELAIS + ' GPIO ' + str(RELAIS_GPIO) +             ' ausgeschaltet             '
                SetText = Fore.BLACK + Back.RED + LogText
        
        if loggen  :                      # Protokollzeile in Logdatei für Relaissteuerung aus GVS anfügen
            LogText = Func_LogDatei.Schreiben (time.strftime("%Y.%m.%d %H:%M:%S") , LogText , GVS.RelLogDir , GVS.RelLogFile)
            if LogText[0:6] == 'Fehler' : # Fehler beim Schreiben der Logdatei
                LogText = Fore.RED   + Back.RESET + Style.BRIGHT + LogText
            else :
                LogText = LogText [20:len(LogText)]  # Log-Text ohne time_stamp anzeigen 
                LogText = 20 * ' ' + Fore.RESET + Back.RESET + Style.BRIGHT + LogText
        
        if drucken :                      # Ausgabe auf Konsole
            SetText = time.strftime("%Y.%m.%d %H:%M:%S") + ' ' + SetText
            SetText = SetText + Style.RESET_ALL
            if loggen :
                return (SetText + '\n' + LogText)
            else :
                return (SetText)
        else :
            return ()
    
    # Fehler festgestellt !
    else :
        SetText = SetText + Style.RESET_ALL
        return (SetText)


def Reset (RELAIS , switch , drucken , loggen) :      # Relais initialisieren / Reset
    wait = 0.5
    if RELAIS == 'alle' :                             # alle aus RelList
        ResetText = 'mit Func_Relais.Reset folgende Relais gemäß RelList in RelTab zurückgesetzt :' 
        ResetText = 20 * ' ' + ResetText + '\n'       # 20 Stellen einrücken , neue Zeile
        for akt_RELAIS in GVS.RelList :
            Ergebnis = Set (akt_RELAIS , switch , drucken , loggen)
            ResetText = ResetText + Ergebnis + '\n'
            time.sleep(wait)
    else :                                            # ein Einzelnes explizit
        ResetText = 'mit Func_Relais.Reset folgendes Relais in RelTab zurückgesetzt :'
        ResetText = 20 * ' ' + ResetText + '\n'       # 20 Stellen einrücken , neue Zeile
        Ergebnis = Set (RELAIS , switch , drucken , loggen)
        ResetText =  ResetText + Ergebnis + '\n'
        time.sleep(wait)
    return (ResetText)

