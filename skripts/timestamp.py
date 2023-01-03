# Platzhalter (strings !)  :

# %a   Abgekürzter Name des Wochentags.
# %A   Vollständiger Name des Wochenstags.
# %b   Abgekürzter Name des Monats.
# %B   Vollständiger Name des Monats.
# %c   Datum und Uhrzeit im Format des lokalen Systems.
# %d   Nummer des Tages im aktuellen Monat [01..31].
# %H   Stunde im 24-Stunden-Format [00..23].
# %I   Stunde im 12-Stunden-Format [01..12].
# %j   Nummer des Tages im Jahr [001..366].
# %m   Nummer des Monats [0.12].
# %M   Minute [00..59].
# %p   Die lokalisierte Form für AM beziehungsweise PM.
# %S   Sekunde [00..61].
# %U   Nummer der aktuellen Woche im Jahr [00..53].
#      Der Sonntag ist der erste Tag der Woche.
#      Der Zeitraum vor dem ersten Sonntag Im Jahr wird als 0. Woche gewertet.
# %w   Nummer das aktuellen Tages in der Woche [0..6].
#      Der Sonntag wird als 0. Tag betrachtet.
# %W   Wie %U, nur dass der Montag der erste Tag der Woche ist.
# %x   Datum im Format des lokalen Systems.
# %X   Zeit im Format des lokalen Systems.

# %y   Jahreszahl ohne Jahrhundertangabe [00..99].
# %Y   Jahreszahl mit Jahrhundertangabe.
# %Z   Name der lokalen Zeitzone oder ein leerer String, wenn keine lokale Zeitzone festgelegt wurde.
# %%   Erzeugt ein Prozentzeichen.

#!/usr/bin/env python

# import time module
import time

# gültiges Systemdatum ?
if int((time.strftime("%Y"))) < 2019 or int((time.strftime("%Y"))) > 2050 :
    print(time.strftime("%d.%m.%Y %H:%M:%S"),"ERROR Entladesteuerung , falsches Systemdatum : ")
    exit
else :
    # print current date and time
    print(time.strftime("%d.%m.%Y %H:%M:%S"),'=============== Start  Entladesteuerung  =======================')
    
