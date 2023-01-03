# -*- coding: utf-8 -*-

import GVS                 # Zwischenspeicher eigene globale Variablen

    # Entscheid , ob fǘr Nachtaufladung Gerät eingeschaltet wird

def pruef (NT_Zeit_Start,NT_Zeit_Ende,Geraetvon,Geraetbis,DTvon,DTbis,DTakt) :       
    Intervall_Fehler = True
    NT_Ladung_Geraet = False
    # NT_Zeit                 Mitternacht                   NT_Zeit
    #  Start   Intervall vor                Intervall nach   Ende
    #   I--------------------------II-----------------------I
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
        
    # bei Intervall-Fehler , Boiler nicht einschalten
    if Intervall_Fehler : NT_Ladung_Geraet = False
  
    GVS.NT_Ladung_Geraet = NT_Ladung_Geraet
    
    return (Intervall_Fehler)
  
#    if Intervall_Fehler :
#        print     ("Boiler NT-Ladung    nicht aktiv , falsche Parameter , keine Nachtladung möglich !")
#        print     ("                    Ladezeit",Geraetvon,'bis',Geraetbis,'außerhalb NT-Intervall',NT_Zeit_Start,'bis',NT_Zeit_Ende)
#        raise ValueError ("daher weitere Verarbeitung nicht möglich")
#        
#    if NT_Ladung_Geraet :
#        if BTakt >= BTmax :
#            NT_Ladung_Geraet = False
#            print ("Boiler NT-Ladung    nicht aktiv max.Temperatur erreicht",BTakt)
#        else :
#            print ("Boiler NT-Ladung    aktiv von",Geraetvon,"bis",Geraetbis,'aktuell',DTakt)
#    else :
#        print     ("Boiler NT-Ladung    nicht aktiv , nur von",Geraetvon,"bis",Geraetbis,'aktuell',DTakt,)
#    
#    
