# shell : python3 /home/pi/skripts/prod/Func_Sens_TEST.py

#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dieses Skript dient zum Test der internen Funktion les_alle_Sens

import time 

from colorama import init , Fore , Style
                    # init(autoreset=True) Farbe gilt nur je Druckposition
                    # init()               Farbe gilt bis Programmende
                    #Farben :
                    #Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Style: DIM, NORMAL, BRIGHT, RESET_ALL
init(autoreset=True)

import Func_Sens # Funktion zum Abfragen der Temperatursensoren


try :
    Sens_Name = 'Raum'
    Ergebnis = str(Func_Sens.Temp(Sens_Name))
    print ('Ergebnis Auslesen eines einzelnen Sensors :')
    print (Sens_Name , Ergebnis)
    if 'Fehler' in Ergebnis :
        raise AssertionError (Ergebnis)
    
    print ()
    Typ = 'DS18B20'
#     Typ = 'unknown'        # für test falscher Typ
    Ergebnis = str(Func_Sens.les_alle (Typ)) 
    print ('Ergebnis Auslesen aller Sensoren :')
    print (Ergebnis)
    if 'Fehler' in Ergebnis :
        raise AssertionError (Ergebnis)
    

except AssertionError as e :
    # Programm ABBRUCH mit AssertionError
    print ()
    END_TEXT   = 'ABBRUCH '
    END_TEXT1  = 'mit AssertionError : '
    END_TEXT2  = str(e)
    END_TEXTZ  = Fore.RED + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + ' '
    END_TEXTZ1 = Fore.RED + Style.BRIGHT + 20 * ' '
    print   (END_TEXTZ  + END_TEXT)                     # 1. Zeile Drucken           
    print   (END_TEXTZ1 + END_TEXT1)                    # 2. Zeile Drucken
    print   (END_TEXTZ1 + END_TEXT2)                    # 3. Zeile Drucken

except Exception as e :
    # Programm ABBRUCH mit Exception
    print ()
    END_TEXT   = 'ABBRUCH '
    END_TEXT1  = 'mit Exception : : '
    END_TEXT2  = str(e)
    END_TEXTZ  = Fore.RED + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + ' '
    END_TEXTZ1 = Fore.RED + Style.BRIGHT + 20 * ' '
    print   (END_TEXTZ  + END_TEXT)                     # 1. Zeile Drucken           
    print   (END_TEXTZ1 + END_TEXT1)                    # 2. Zeile Drucken
    print   (END_TEXTZ1 + END_TEXT2)                    # 3. Zeile Drucken

