# shell : python3 /home/pi/skripts/prod/Func_Relais_manuell.py
#!/usr/bin/python3
# -*- coding: utf-8 -*- 
#
# Programm zum manuellen Schalten , Initialisieren bzw. Testen einzelner Relais

import Func_Relais              # Funktion zum Set / Reset der Relais

# Setzen Parameter zur Ein-/Aus-Schaltung eines einzelnen Relais
drucken      = True           # True = ja , False = nein
loggen       = True           # aus RelTab oder True = ja , False = nein
RELAIS       = 'WK4'          # Relais wie in Relais-Tabelle GVS.RelTab() definiert
# Schaltvorgang durchführen Schalten , ggf.Ergebnis drucken , lpggen
Schalter     = True           # True = ein , False = aus
print ('Ergebnis nach Vorgang Schaltung eines einzelnen Relais :')
print (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))

## Schaltvorgang durchführen Ausschalten , Ergebnis drucken
#Schalter     = False            # True = ein , False = aus
#print (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))

# # Setzen Parameter zur Initialisierung eines einzelnen Relais
# drucken      = True           # True = ja , False = nein
# loggen       = True           # aus RelTab ober True = ja , False = nein
# RELAIS       = 'WK3'          # Relais wie in Relais-Tabelle GVS.RelTab() definiert
# # Initialisierung durchführen Schalten , ggf.Ergebnis drucken , lpggen
# Schalter     = True         # True = ein , False = aus
# print ()
# print ('Ergebnis nach Vorgang Initialisierung eines einzelnen Relais :')
# print (Func_Relais.Reset (RELAIS , Schalter , drucken , loggen))

# Setzen Parameter zur Initialisierung aller Relais
drucken      = True           # True = ja , False = nein
loggen       = True           # aus RelTab ober True = ja , False = nein
RELAIS       = 'alle'         # alle Relais wie in Relais-Tabelle GVS.RelTab() definiert
# Initialisierung durchführen Schalten , ggf.Ergebnis drucken , lpggen
Schalter     = False         # True = ein , False = aus
print ()
print ('Ergebnis nach Vorgang Initialisierung aller Relais  :')
print (Func_Relais.Reset (RELAIS , Schalter , drucken , loggen))
