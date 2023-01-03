# shell : python3 /home/pi/skripts/prod/Geraet_Test.py
#         @/usr/bin/python3 /home/pi/skripts/prod.Entladesteuerung.py

# -*- coding: utf-8 -*-   


##   T E S T Programm     ###########################################################################################


######################################### Beginn UP Geraet prüfen ########################################################## 
def Geraet_pruef (Geraet,NT_Z_Start,NT_Z_Ende,G_Z_von,G_Z_bis,T_Z_von,T_Z_bis,T_Z_akt,G_T_akt,G_T_min,G_T_max,G_T_hist) :
    Schalt_Rel   = ''
    Rel_Schalter = ''
    Fehler       = ''
    liste        = [Schalt_Rel , Rel_Schalter , Fehler]
    
    # nur Geraet und Boiler als Geräte zulässig !
    if   Geraet == 'Kessel' :
        Rel_Geraet    = 'KK2'                               # Relais Keller Kessel komplett
        Rel_Ger_DL    = 'DK2'                               # Relais für Kessel Direktladung
        Hist_Schalter = 'DK2_Hist'                          # Histerese-Schalter für Kessel Direktladung
        Rel_Ger_NL    = 'HK2'                               # Relais für Nachtladung Kessel
    elif Geraet == 'Boiler' :
        Rel_Geraet    = 'KK1'                               # Relais Keller Boiler komplett
        Rel_Ger_DL    = 'DK1'                               # Relais für Boiler Direktladung
        Hist_Schalter = 'DK1_Hist'                          # Histerese-Schalter für Boiler Direktladung
        Rel_Ger_NL    = 'BK1'                               # Relais für Nachtladung Boiler
    else :                                                  # Abbruch , da Programmfehler unzulässiges Gerät
        Fehler =  ' falsche Gerätedefinition "' + Geraet + '" , nur "Geraet" oder "Boiler" zulässig'
        liste = [Schalt_Rel , Rel_Schalter , Fehler]
        return (liste)
    # Ausgabe Geraettemperatur , Prüfung , ob Histerese ein / aus / bleibt
    TextString = '- ' + Geraet + 'temperatur  aktuell ' + str(G_T_akt) + ' max ' + str(G_T_max) + ' min ' + str(G_T_min) 
    TextString = TextString + ' Histerese ' + str(G_T_hist)
    print (TextString)
    # Prüfung Plausibilität der Ladezeiten und ob für Nachtaufladung Geraet einzuschalten ist               
    NT_Lad_Geraet = Func_NT_Ladung.pruef (NT_Z_Start,NT_Z_Ende,G_Z_von,G_Z_bis,T_Z_von,T_Z_bis,T_Z_akt,G_T_akt,G_T_max)
    print (NT_Lad_Geraet)
    if   "-- Nachtladung      nicht" in NT_Lad_Geraet :   # Nachtladung nicht aktiv
        Schalt_Rel   = Rel_Geraet                         # Relais Geraet komplett abschalten
        Rel_Schalter = False                              # Relais Schalter aus
        # Entscheid , ob fǘr Direktladung Geraet eingeschaltet wird
        # Direktladung nur , wenn keine Nachtladung eingeschaltet = Histerese läuft
        # prüfen ob Histerese beginnt , endet , läuft
        Dir_Lad_Geraet = Func_Hist.pruef (G_T_akt,G_T_min,G_T_hist,Hist_Schalter)
        if   "läuft" in Dir_Lad_Geraet :          # Direktladung läuft
            Schalt_Rel   = Rel_Ger_DL             # Relais für Geraet Direktladung verwenden
            Rel_Schalter = True                   # Relais Schalter ein
            TextString = "-- Direktladung     aktiv aktuell " + str(G_T_akt) + " war gefallen unter Minimum " + str(G_T_min)
            TextString = Fore.YELLOW + TextString
        elif "ausgeschaltet" in Dir_Lad_Geraet :  # Direktladung ausgeschaltet                                                            # Direktladung läuft nicht
            TextString = "-- Direktladung     nicht aktiv"
        else :                                    # Abbruch , da Programmfehler
            Fehler =  ' Direktladung ' + Geraet + Dir_Lad_Geraet
            liste = [Schalt_Rel , Rel_Schalter , Fehler]
            return (liste)
        print (TextString,Dir_Lad_Geraet)
        
    elif "-- Nachtladung      aktiv" in NT_Lad_Geraet :   # Nachtladung aktiv
        Schalt_Rel   = Rel_Ger_NL                         # Relais für Nachtladung Geraet verwenden
        Rel_Schalter = True                               # Relais Schalter ein
        GVS.RelTab[Hist_Schalter] = False                 # bei NT-Ladung keine Histerese
        TextString = "-- Direktladung     nicht aktiv , da Nachtaufladung"
        print (TextString)
    else :                                                # Abbruch , da Programmfehler
        Fehler =  ' Nachtaufladung ' + Geraet + NT_Lad_Geraet
        liste = [Schalt_Rel , Rel_Schalter , Fehler]
        return (liste)
    
    liste = [Schalt_Rel , Rel_Schalter , Fehler]
    
    return (liste)
    
######################################### Ende UP Geraet prüfen ############################################################        

###################################### Beginn Hauptprogramm neu #####################################################

import Func_NT_Ladung , GVS , Func_Hist
from colorama import init , Fore , Style , Back

NT_Zeit_Start = '22:00'
NT_Zeit_Ende  = '06:00'
KNvon         = '22:15'
KNbis         = '23:00'
DTvon         = '09:00'
DTbis         = '16:00'
DTakt         = '03:00'
KTakt         = 39.1
KTmin         = 40.0
KTmax         = 65.0
KThist        =  3.0

Verbr         = 'Boiler'

Ergebnis = Geraet_pruef(Verbr,NT_Zeit_Start,NT_Zeit_Ende,KNvon,KNbis,DTvon,DTbis,DTakt,KTakt,KTmin,KTmax,KThist)

Rel_NameBoiler    = Ergebnis.pop(0)   # 1. Parameter des Ergebnisses : betreffendes Relais
Rel_SchBoiler     = Ergebnis.pop(0)   # 2. Parameter des Ergebnisses : betreffender Schalter
e                 = Ergebnis.pop(0)   # 3. Parameter des Ergebnisses : Fehlermeldung bei Abbruch
   
if e != '' :                    # Abbruch bei Programmfehler
    raise AssertionError (e) 
else :
    print ()
    print ('Ergebnis für Geraet_pruef ',Verbr)
    print ()
    print ('zu schaltendes Relais      : ',Rel_NameBoiler)
    print ('Schalter für   Relais      : ',Rel_SchBoiler)

###################################### Ende Hauptprogramm neu #######################################################

###################################### Ende Testprogramm #############################################################