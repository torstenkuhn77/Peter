# shell : python3 /home/pi/skripts/prod/Func_Geraet.py
#         @/usr/bin/python3 /home/pi/skripts/prod.Func_Geraet.py

#!/usr/bin/python3
# -*- coding: utf-8 -*-   

import Func_NT_Ladung , GVS , Func_Hist
    
# Bedeutung der Parameter :
# Geraet                 Boiler oder Kessel
# NT_Z_Start/Ende        Niedertarif - Zeiten
# G_Z_von/bis            Zeit , während der der Nieder-Tarif vom Gerät genutzt werden soll
# T_Z_von/bis/akt        Tag - Zeiten
# G_T_akt/min/max/hist   Geräte - Temperaturen

######################################### Beginn UP Geraet prüfen ##########################################################

def pruef (Geraet,NT_Z_Start,NT_Z_Ende,G_Z_von,G_Z_bis,T_Z_von,T_Z_bis,T_Z_akt,G_T_akt,G_T_min,G_T_max,G_T_hist) :
    Schalt_Rel   = ''
    Rel_Schalter = ''
    TextString   = ''
    liste        = [Schalt_Rel , Rel_Schalter , TextString]
    
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
        TextString =  'Fehler in Funktion Gerät.pruef : "' + Geraet + '" , nur "Kessel" oder "Boiler" zulässig'
        liste = [Schalt_Rel , Rel_Schalter , TextString]
        return (liste)
    # Ausgabe Geraetetemperatur , Prüfung , ob Histerese ein / aus / bleibt
    TextString = '- ' + Geraet + 'temperatur  oben ' + str(G_T_akt) + ' max ' + str(G_T_max) + ' min ' + str(G_T_min) 
    TextString = TextString + ' Histerese ' + str(G_T_hist)
    # Prüfung Plausibilität der Ladezeiten und ob für Nachtladung Geraet einzuschalten ist               
    NT_Lad_Geraet = Func_NT_Ladung.pruef (NT_Z_Start,NT_Z_Ende,G_Z_von,G_Z_bis,T_Z_von,T_Z_bis,T_Z_akt,G_T_akt,G_T_max)
    TextString = TextString + '\n'                        # neue Zeile
    TextString = TextString + NT_Lad_Geraet
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
            TextString = TextString + '\n'        # neue Zeile
            TextString = TextString + "-- Direktladung     aktiv aktuell " + str(G_T_akt) + " war gefallen unter Minimum " + str(G_T_min)
            TextString = TextString + '\n'        # neue Zeile
            TextString = TextString + 20 * ' ' + Dir_Lad_Geraet
        elif "ausgeschaltet" in Dir_Lad_Geraet :  # Direktladung ausgeschaltet , läuft nicht
            TextString = TextString + '\n'        # neue Zeile
            TextString = TextString + "-- Direktladung     nicht aktiv , Temperatur blieb oberhalb Minimum " + str(G_T_min)
        else :                                    # Abbruch , da Programmfehler
            TextString =  'Fehler in Funktion Hist.pruef : "' + Geraet + '" ' + Dir_Lad_Geraet
#            liste = [Schalt_Rel , Rel_Schalter , TextString]
#            return (liste)
        
    elif "-- Nachtladung      aktiv" in NT_Lad_Geraet :   # Nachtladung aktiv
        Schalt_Rel   = Rel_Ger_NL                         # Relais für Nachtladung Geraet verwenden
        Rel_Schalter = True                               # Relais Schalter ein
        GVS.RelTab[Hist_Schalter] = False                 # bei NT-Ladung keine Histerese
        TextString = TextString + '\n'                    # neue Zeile
        TextString = TextString + "-- Direktladung     nicht aktiv , da Nachtladung"
    else :                                                # Abbruch , da Programmfehler
        TextString =  'Fehler in Funktion NT_Ladung.pruef : "' + Geraet + '" ' + NT_Lad_Geraet
#        liste = [Schalt_Rel , Rel_Schalter , TextString]
#        return (liste)
    
    liste = [Schalt_Rel , Rel_Schalter , TextString]
    
    return (liste)
    
######################################### Ende UP Geraet prüfen ############################################################        

