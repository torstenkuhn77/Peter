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
    Mitternacht      = '00:00'
    NT_Ladung_Geraet = False
    Ergebnis         = ''
    # Prüfung Intervall Nachtladung
    # NT_Zeit                 Mitternacht                 NT_Zeit
    #  Start   Intervall vor               Intervall nach  Ende
    #   I--------------------------II------------------------I
    # "von" und "bis" im Intervall vor Mitternacht :
    if   Geraetvon >= NT_Zeit_Start and Geraetbis < Mitternacht :
        if Geraetbis < Geraetvon :
            Ergebnis = ' fehlerhaftes Geräte-Intervall ' + Geraetvon + ' bis ' + Geraetbis + '(' + NT_Zeit_Start + '-' + Mitternacht + ')'
        if DTakt >= Geraetvon and DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # "von" und "bis" im Intervall nach Mitternacht:
    elif Geraetvon >= Mitternacht and Geraetbis <= NT_Zeit_Ende :
        if Geraetbis < Geraetvon :
            Ergebnis = ' fehlerhaftes Geräte-Intervall ' + Geraetvon + ' bis ' + Geraetbis + '(' + Mitternacht + '-' + NT_Zeit_Ende + ')'
        if DTakt >= Geraetvon and DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # "von" im Intervall vor , "bis" im Intervall nach Mitternacht:
    elif Geraetvon >= NT_Zeit_Start and Geraetvon < Mitternacht and Geraetbis >= Mitternacht and Geraetbis <= NT_Zeit_Ende :
        if DTakt >= Geraetvon or DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # Intervall nicht plausibel:
    else :
        Ergebnis = ' fehlerhaftes Geräte-Intervall ' + Geraetvon + ' bis ' + Geraetbis + ' im NT-Intervall ' + NT_Zeit_Start + ' bis ' + NT_Zeit_Ende
        
    # bei Intervall-Fehler :  Abbruch , Rückgabe Fehlermeldung
    if Ergebnis != '' :
        Ergebnis = Fore.RED + Ergebnis + Fore.RESET
        return (Ergebnis)
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
            Ergebnis =     "-- Nachtladung      nicht aktiv im Geräte-Intervall " + Geraetvon + " bis " + Geraetbis
            Ergebnis =      Ergebnis + ' im NT-Intervall ' + NT_Zeit_Start + ' bis ' + NT_Zeit_Ende + ' um ' + DTakt 
        
    return (Ergebnis)


