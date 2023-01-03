# shell : python3 /home/pi/skripts/prod/Func_Solar_Log_TEST.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# skript zum Testen der Funktion Func_Solar_Log

import Func_Solar_Log    # Funktion zum Lesen aus Solar-Log JSON
import GVS               # Zwischenspeicher eigene globale Variablen

# lokale fixe IPV4 Adresse :
# 169.254.xx.yy letzte 4 Stellen = letzte 4 Stellen der SN des Solar-Log
# hier Seriennummer 1350323432 --> 169.254.34.32
# alternativ DHCP-Adresse aus dem lokalen Netzwerk verwenden

SolarLog_localIP = GVS.SolarLog_localIP            # lokale IP des Solar-Log
SoLo_Text = Func_Solar_Log.Lesen(SolarLog_localIP) # Solar-log JSON lesen

print (SoLo_Text)                                  # Text Drucken
print ('Verbrauch   ',GVS.SolarLog_Verbrauch)
print ('Erzeugung   ',GVS.SolarLog_Erzeugung)

Bilanz = (round((GVS.SolarLog_Erzeugung - GVS.SolarLog_Verbrauch),2))

if Bilanz >= 0 :
    print('Einspeisung ',Bilanz,'   (Erzeugung - Verbrauch)')    
else :
    print('Bezug       ',Bilanz,'   (Erzeugung - Verbrauch)')

