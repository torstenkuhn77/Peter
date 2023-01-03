# shell :  python3 /home/pi/skripts/Func_Relais_Test.py
# Test Programm zum Ein-/Ausschalten eines Relais mit Bezeichnung 'xyz'

import Func_Relais 

# Setzen Parameter zur Schaltung von Relais für die Funktion

# def Schaltung (RELAIS , Schalter , drucken , loggen)

# Schaltvorgang durchführen : Einschalten mit korrekten Angaben --> Log
RELAIS       = 'WK4'   # Relais wie in Relais-Tabelle definiert
Schalter     = True    # zulässig : ein , aus
drucken      = True    # True = ja , False = nein
loggen       = True    # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))

# Schaltvorgang durchführen : erneut Einschalten mit korrekten Angaben --> kein Log
RELAIS       = 'WK4'   # Relais wie in Relais-Tabelle definiert
Schalter     = True    # zulässig : ein , aus
drucken      = True    # True = ja , False = nein
loggen       = True    # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))

# Schaltvorgang durchführen : Ausschalten mit korrekten Angaben --> Log
RELAIS       = 'WK4'   # Relais wie in Relais-Tabelle definiert
Schalter     = False   # zulässig : ein , aus
drucken      = True    # True = ja , False = nein
loggen       = True    # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))

# Schaltvorgang durchführen : erneut Ausschalten mit korrekten Angaben --> kein Log
RELAIS       = 'WK4'   # Relais wie in Relais-Tabelle definiert
Schalter     = False   # zulässig : ein , aus
drucken      = True    # True = ja , False = nein
loggen       = True    # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))

# Auslösen von Fehlern falsches Relais
RELAIS       = 'WK9'
Schalter     = True
drucken      = True    # True = ja , False = nein
loggen       = True    # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))

# Auslösen von Fehlern falscher Schalter , falsches Relais
RELAIS       = 'WK9'
Schalter     = 'ping'
drucken      = True    # True = ja , False = nein
loggen       = True    # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))

# Auslösen von Fehlern falsche Schalter , falsches Relais
RELAIS       = 'WK9'
Schalter     = 'ping'
drucken      = 'ohweh' # True = ja , False = nein
loggen       = 'hurra' # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))

# Auslösen von Fehlern richtiges Relais , richtiger Schalter keine Funktion definiert in GVS
RELAIS       = 'BK1'
Schalter     = False
drucken      = True    # True = ja , False = nein
loggen       = True    # True = ja , False = nein
print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))
