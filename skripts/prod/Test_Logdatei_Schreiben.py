# shell : python3 /home/pi/skripts/prod/Test_Logdatei_Schreiben.py

# die Farbsteuerung funktioniert nur bei Ausführung aus der Konsole !
# Beschreibung : https://pypi.org/project/colorama/

# Programm zum Testen der Funktion Func_LogDatei  # eigene Funktion Logdatei schreiben

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


StartText = 'Neustart Entladesteuerung ... '
print (Style.BRIGHT + StartText)
LogText = Func_LogDatei.Schreiben (time.strftime("%Y.%m.%d %H:%M:%S") , StartText , GVS.RelLogDir , GVS.RelLogFile)
if LogText[0:6] == 'Fehler' : # Fehler beim Schreiben der Logdatei
    StartText = Fore.RED  + Back.RESET + Style.BRIGHT + LogText
else :
#     LogText = LogText [20:len(LogText)]  # Log-Text ohne time_stamp
#     LogText = 20 * ' ' + Fore.RESET + Back.RESET + Style.BRIGHT + LogText
    StartText = Fore.RESET + Back.RESET + Style.BRIGHT + LogText
print (StartText)
