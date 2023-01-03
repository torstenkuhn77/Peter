# Funktion zur Prüfung , ob die Schaltzeiten für Nachtaufladung plausibel sind und das Gerät eingeschaltet werden kann

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from colorama import Fore 

# Parameter :
# NT_Zeit_Start,NT_Zeit_Ende  :  Start,Ende Niedertarifzeit
# Geraetvon,Geraetbis         :  Start,Ende der Ladezeit des Gerätes
# DTvon,DTbis,DTakt           :  Start,Ende Tagsteuerung , aktuelle Tageszeit
# GeraeTakt,GeraeTmax         :  Temperatur des Gerätes aktuell,maximal

def pruef (NT_Zeit_Start,NT_Zeit_Ende,Geraetvon,Geraetbis,DTvon,DTbis,DTakt,GeraeTakt,GeraeTmax) :          
    # Initialisierung
    Intervall_Fehler = True
    NT_Ladung_Geraet = False
    Ergebnis         = ''
    # Prüfung Intervall Nachtladung
    # NT_Zeit                 Mitternacht                 NT_Zeit
    #  Start   Intervall vor               Intervall nach  Ende
    #   I--------------------------II------------------------I
    # "von" und "bis" im Intervall vor Mitternacht :
    if   Geraetvon >= NT_Zeit_Start and Geraetbis <= "23:59" :
        if Geraetbis > Geraetvon : Intervall_Fehler = False
        if Geraetvon <= DTbis    : Intervall_Fehler = True
        if DTakt >= Geraetvon and DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # "von" und "bis" im Intervall nach Mitternacht:
    elif Geraetvon >= "00:00" and Geraetbis <= NT_Zeit_Ende :
        if Geraetbis > Geraetvon : Intervall_Fehler = False
        if Geraetbis >= DTvon    : Intervall_Fehler = True
        if DTakt >= Geraetvon and DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # "von" im Intervall vor , "bis" im Intervall nach Mitternacht:
    elif Geraetvon >= NT_Zeit_Start and Geraetvon <= "23:59" and Geraetbis >= "00:00" and Geraetbis <= NT_Zeit_Ende :
        Intervall_Fehler = False
        if Geraetvon <= DTbis or Geraetbis >= DTvon : Intervall_Fehler = True
        if DTakt >= Geraetvon or DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # Intervall nicht plausibel:
    else :
        Intervall_Fehler = True
        
    # bei Intervall-Fehler , Rückgabe Fehlermeldung
    if Intervall_Fehler :
        Ergebnis =         " fehlerhaftes Intervall " + Geraetvon + ' bis ' + Geraetbis
    # Entscheid , ob Nachtladung aktiv oder nicht
    else :
        if NT_Ladung_Geraet :   # Wenn Nachtladung innerhalb definierter Zeiten möglich :
            if GeraeTakt >= GeraeTmax :
                Ergebnis = "-- Nachtladung      nicht aktiv , max.Temperatur " + str(GeraeTmax) + " erreicht bei " + str(GeraeTakt) + ' Grad'
            else :
                Ergebnis = "-- Nachtladung      aktiv von " + Geraetvon + " bis " + Geraetbis + ' aktuell ' + DTakt
                Ergebnis = Ergebnis + ' bis max ' + str(GeraeTmax) + ' Grad'
                Ergebnis = Fore.YELLOW + Ergebnis + Fore.RESET
        else :                  # Wenn Nachtladung innerhalb definierter Zeiten nicht möglich :
            Ergebnis =     "-- Nachtladung      nicht aktiv im Intervall " + Geraetvon + " bis " + Geraetbis
        
    return (Ergebnis)


