# Funktion zur Prüfung Histerese : "läuft" oder "ausgeschaltet" oder Fehler

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import GVS            # Zwischenspeicher eigene globale Variablen

def pruef (Takt, Tmin, Thist, Index):       

#            Takt  = aktuelle Temperatur
#            Tmin  = minimale Temperatur
#            Thist = Histerese
#            Index = DK1_Hist bei Boiler , DK2_Hist bei Kessel
            
    Text = 'Fehler bei Überprüfung der Histerese '
    
    if Takt <= Tmin :                            # aktuelle Temperatur auf/unter Minimum gesunken
                                                 # Änderung des Status der Histerese wird oder bleibt eingeschaltet
        if GVS.RelTab[Index] :                   # Histerese war ein - und bleibt eingeschaltet
            Text = f"--> Histerese (+{Thist}) läuft weiter bis {Tmin + Thist}"
        else :                                   # Histerese wird erstmals eingeschaltet
            Text = f"--> Histerese (+{Thist}) läuft an bei {Takt} und weiter bis {Tmin + Thist}" 
        GVS.RelTab[Index] = True    
    if Takt > Tmin and Takt < (Tmin + Thist) :   # aktuelle Temperatur zwischen Minimum und Minimum + Histerese
                                                 # keine  Änderung des Status der Histerese
        if GVS.RelTab[Index] :                   # Histerese war ein - und bleibt eingeschaltet
            Text = f"--> Histerese (+{Thist}) läuft weiter bis {Tmin + Thist}"
        else :                                   # Histerese war aus - und bleibt ausgeschaltet
            Text = f"--> Histerese ausgeschaltet , wird erst bei {Tmin} wieder aktiviert"
            
    if Takt >= (Tmin + Thist) :                  # aktuelle Temperatur über Histerese gestiegen
                                                 # Änderung des Status der Histerese wird oder bleibt ausgeschaltet
        if GVS.RelTab[Index] :                   # Histerese war ein - wird ausgeschaltet
            Text = f"--> Histerese lief bis {Tmin + Thist} , wurde bei {Takt} ausgeschaltet"
        else :                                   # Histerese war aus - und bleibt ausgeschaltet
            Text = f"--> Histerese ausgeschaltet , wird erst bei {Tmin} wieder aktiviert"
        GVS.RelTab[Index] = False                # Histerese endet
    
    return True                       # Histerese / Direktladung läuft
 ################## Histerese prüfen Ende  ###################################################################################
