# Funktion zur Prüfung , ob die Schaltzeiten für Nachtaufladung plausibel sind und das Gerät eingeschaltet werden kann

#!/usr/bin/python3
# -*- coding: utf-8 -*-



    # Entscheid , ob fǘr Nachtaufladung Gerät eingeschaltet wird

def pruef (NT_Zeit_Start,NT_Zeit_Ende,Geraetvon,Geraetbis,DTvon,DTbis,DTakt) :       
    Intervall_Fehler = True
    NT_Ladung_Geraet = False
    # NT_Zeit                 Mitternacht                 NT_Zeit
    #  Start   Intervall vor               Intervall nach  Ende
    #   I--------------------------II------------------------I
    # "von" und "bis" im Intervall vor Mitternacht :
    if Geraetvon >= NT_Zeit_Start and Geraetbis <= "23:59" :
        if Geraetbis > Geraetvon : Intervall_Fehler = False
        if Geraetvon <= DTbis : Intervall_Fehler = True
        if DTakt >= Geraetvon and DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # "von" und "bis" im Intervall nach Mitternacht:
    if Geraetvon >= "00:00" and Geraetbis <= NT_Zeit_Ende :
        if Geraetbis > Geraetvon : Intervall_Fehler = False
        if Geraetbis >= DTvon : Intervall_Fehler = True
        if DTakt >= Geraetvon and DTakt <= Geraetbis : NT_Ladung_Geraet = True
    # "von" im Intervall vor , "bis" im Intervall nach Mitternacht:
    if Geraetvon >= NT_Zeit_Start and Geraetvon <= "23:59" and Geraetbis >= "00:00" and Geraetbis <= NT_Zeit_Ende :
        Intervall_Fehler = False
        if Geraetvon <= DTbis or Geraetbis >= DTvon : Intervall_Fehler = True
        if DTakt >= Geraetvon or DTakt <= Geraetbis : NT_Ladung_Geraet = True
        
    # bei Intervall-Fehler , Gerät nicht einschalten
    if Intervall_Fehler :     Ergebnis = ' fehlerhaftes Intervall ',Geraetvon,' bis ',Geraetbis
    else :
        if NT_Ladung_Geraet : Ergebnis = 'ein'
        else :                Ergebnis = 'aus'
        
    # Rückgabe ein für Einschalten , aus für Ausschalten , sonst Fehler
    return (Ergebnis)
