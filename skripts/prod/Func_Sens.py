# shell : python3 /home/pi/skripts/prod/Func_Sens_neu.py

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

import GVS      # Zwischenspeicher eigene globale Variablen

from colorama import init , Fore , Style
init(autoreset=True) # init(autoreset=True) Farbe gilt nur je Druckposition
                     # init()               Farbe gilt bis Programmende
# Farben Vordergrund # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Farben Hintergrund # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                     # Style: DIM, NORMAL, BRIGHT, RESET_ALL


def les_alle (Typ) :   # aus Systembus alle Temperaturen zu allen Sensoren eines Typs auslesen
                       # und in GVS.SensTab speichern und Rückgabe zum Druck aufbereiteter Textzeilen
    if Typ not in 'DS18B20' :             # vorläufig nur dieser Typ zulässig
        Text = 'Fehler in Func_Sens.les_alle : Sensor Typ "' + Typ + '" nicht zulässig'
        return (Text)
    
    Lesefehler = False                    # Annahme : es wird kein Lesefehler auftreten
    Text    = ''                          # init Text für Druck / return
    TextOK  = ''                          # init Text erfolgreich ausgelesene Sensoren
    TextNOK = ''                          # init Text nicht erfolgreich ausgelesene Sensoren 
    
    for SEN in GVS.SensList :             # Temperaturwerte aller Sensoren auslesen                                                                        
        Ergebnis  = Temp (SEN)            # Temperaturwert des einzelnen Sensors auslesen
        GVS.SensTab [SEN + '_Tmp'] = Ergebnis
                                          # Prüfung , ob ausgelesener Wert fehlerhaft
        if Ergebnis == 0 or 'Fehler' in (str(Ergebnis)) : # JA : fehlerhaft ausgelesen
            GVS.SensTab [SEN + '_Stp'] = 'Fehler beim Auslesen'
            Lesefehler = True                    # --> mindestens ein Lesefehler aufgetreten
            # Textzeilen NOK fehlerhafte Sensoren aufbereiten
            TextNOK = TextNOK + ' ' + str(GVS.SensTab.get(SEN + '_Stp'))      # timestamp = Fehler ...
            TextNOK = TextNOK + ' ' + SEN                                     # Sensor
            TextNOK = TextNOK + ' ' + '\n'                                    # neue Zeile
            TextNOK = TextNOK + 20 * ' '+ str(GVS.SensTab.get(SEN + '_Tmp'))  # einrücken , Temperaturwert
            TextNOK = TextNOK + ' ' + '\n' + 20 * ' '                         # neue Zeile , einrücken
        else :                                            # NEIN : nicht fehlerhaft ausgelesen
            GVS.SensTab [SEN + '_Stp'] = time.strftime("%Y.%m.%d %H:%M:%S")
            # Textzeilen OK fehlerfreie Sensoren aufbereiten
            TextOK  = TextOK + ' ' + SEN                                      # Sensor
            TextOK  = TextOK + ' ' + str(GVS.SensTab.get(SEN + '_Tmp')) + ' ' # Temperaturwert in gleicher Zeile
                
    if Lesefehler :                               # ist mindestens ein Lesefehler aufgetreten ?
        Text = Fore.RED + Style.BRIGHT 
        Text = Text + 'beim Auslesen der Sensoren ' + Typ + ' ist mindestens ein Fehler aufgetreten :' + '\n'
        Text = Text + Fore.GREEN + 19 * ' ' + TextOK + '\n' + Fore.RED + Style.BRIGHT + 20 * ' ' + TextNOK
    else :                                        # kein Lesefehler aufgetreten
        Text = Fore.GREEN + time.strftime("%Y.%m.%d %H:%M:%S")
        Text = Text + ' Temperatur aller Sensoren ' + Typ + ' gespeichert in GVS.SensTab :' + '\n'
        Text = Text + Fore.GREEN + 19 * ' ' + TextOK
    
    return (Text)  # Rückgabe zum Druck aufbereiteter Textzeilen      
    # Ende aus Systembus alle Temperatursensoren eines Typs auslesen und in GVS.SensTab speichern

def Temp(Bez) : # Aus Systembus Temperatur eines einzelnen Sensors auslesen

    if Bez not in GVS.SensTab.keys() :
        return ('Fehler in Func_Sens.Temp : "' + Bez +
                '" nicht in Tabelle Temperatursensoren (GVS.SensTab)')
    if Bez not in GVS.SensList :
        return ('Fehler in Func_Sens.Temp : "' + Bez +
                '" nicht in Liste Temperatursensoren (GVS.SensList)')
    else :   
        # Aus Systembus Temperatursensoren DS18B20 auslesen
        line1und2 = LesBus (str(GVS.SensTab.get(Bez))) # Liste füllen
        line1 = line1und2.pop(0)                       # Liste entladen       
        line2 = line1und2.pop(0)
        if 'Fehler' in line1 : # Abbruch bei Lesefehler im Systembus
            return (line1+line2)
        else :
            # Position von t=..... in der 2. Zeile finden
            temperaturStr = line2.find('t=')   # t=..... finden
            tempData = line2[temperaturStr+2:]
            # auf 1 Nachkommastelle runden
            tempCelsius   = round(float(tempData) / 1000,1)
            if tempCelsius <= 0 :
                return ('Fehler in Func_Sens.Temp : "' + Bez +
                '" Wert ' + str(tempCelsius) + ' ausgelesen , sollte > 0 sein')
            # Korrekturwert des Sensors dazu addieren
            tempCelsius_r = round(tempCelsius +
                            float(str(GVS.SensTab.get(Bez + '_Kor'))) ,1)            
            return (tempCelsius_r)


def LesBus(Index) :                # Systembus lesen , 2 Zeilen je Sensor
    line1     =''                  # Initialisierung
    line2     = ''
    line1und2 = [line1,line2]      # beide Zeilen nin Liste
    i         = 0
    imax      = 2                  # max Leseversuche / Iterationen
    iwait     = 0.5                # Sekunden warten bei Iteration
        
    # Lesen , ggf. Nachlesen , falls keine Temperatur gefunden
    while 'YES' not in line1 or 't=' not in line2 :
        i = i + 1
        if i > 1 : time.sleep (iwait) # mit Nachlesen warten !
        try :
            f = open(Index, 'r')
        except IOError  :            # Abbruch , da Nachlesen erfolglos
            line1 = 'Fehler im Skript Func_Sens.Temp.LesBus :' + '\n' 
            line2 = 20*' ' + 'Index ' + Index + '\n' 
            line2 = line2 + 20*' ' + 'konnte im one-wire bus nicht ausgelesen werden '
            line1und2 =[line1,line2]
            return (line1und2)        # Abbruch , Rückgabe Fehler in Liste
        line1 = f.readline()          # 1. Zeile lesen
        line2 = f.readline()          # 2. Zeile lesen
        line1und2 = [line1,line2]     # Liste erstellen
        f.close()
        if i > imax :                 # Abbruch , da Nachlesen erfolglos
            line1 = 'Fehler im Skript Func_Sens.Temp.LesBus '
            line2 = str(imax) + ' Iterationen überschritten' 
            line1und2 =[line1,line2]
            return (line1und2)        # Abbruch , Rückgabe Fehler in Liste
    
    return (line1und2)                # fehlerfreies Ergebnis als Liste zurück

