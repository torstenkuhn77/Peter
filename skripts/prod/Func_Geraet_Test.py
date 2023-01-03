# shell : python3 /home/pi/skripts/prod/Func_Geraet_Test.py
#         @/usr/bin/python3 /home/pi/skripts/prod.Entladesteuerung.py

# -*- coding: utf-8 -*-   


##   T E S T Programm     ###########################################################################################



###################################### Beginn Hauptprogramm neu #####################################################

import Func_Geraet
from colorama import init 
init(autoreset=True)

NT_Zeit_Start = '22:00'  # Niedertarif - Zeit
NT_Zeit_Ende  = '06:00'
KNvon         = '00:15'  # Geräte - Zeit Niedertemperatur
KNbis         = '05:45'
DTvon         = '08:30'  # Tag - Zeit
DTbis         = '16:00'
DTakt         = '01:00'
KTakt         = 39.1     # Gerätetemperatur
KTmin         = 40.0
KTmax         = 65.0
KThist        =  3.0

Verbr         = 'Boiler' # Gerät

Ergebnis = Func_Geraet.pruef(Verbr,NT_Zeit_Start,NT_Zeit_Ende,KNvon,KNbis,DTvon,DTbis,DTakt,KTakt,KTmin,KTmax,KThist)

Rel_NameBoiler    = Ergebnis.pop(0)   # 1. Parameter des Ergebnisses : betreffendes Relais
Rel_SchBoiler     = Ergebnis.pop(0)   # 2. Parameter des Ergebnisses : betreffender Schalter
e                 = Ergebnis.pop(0)   # 3. Parameter des Ergebnisses : Fehlermeldung bei Abbruch

if 'Fehler' in e :                    # Abbruch bei Programmfehler
    raise AssertionError (e) 
else :
    print ()
    print (e)
    print ()
    print ('Ergebnis für Funktion Geraet_pruef ',Verbr)
    print ()
    print ('zu schaltendes Relais      : ',Rel_NameBoiler)
    print ('Schalter für   Relais      : ',Rel_SchBoiler)
    print ()

###################################### Ende Hauptprogramm neu #######################################################

###################################### Ende Testprogramm #############################################################