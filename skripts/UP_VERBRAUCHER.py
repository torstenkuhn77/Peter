######################################### Beginn UP Geraet ########################################################## 
def Verbraucher (Geraet,NT_Z_Start,NT_Z_Ende,G_Z_von,G_Z_bis,T_Z_von,T_Z_bis,T_Z_akt,G_T_akt,G_T_min,G_T_max,G_T_hist) :
    # nur Geraet und Boiler als Geräte zulässig !
    if   Geraet == 'Kessel' :
        Rel_Geraet    = 'KK2'                               # Relais Keller Kessel komplett
        Rel_Ger_DL    = 'DK2'                               # Relais für Kessel Direktladung
        Hist_Schalter = 'DK2_Hist'                          # Histerese-Schalter für Kessel Direktladung
        Rel_Ger_NL    = 'HK2'                               # Relais für Nachtladung Kessel
    elif Geraet == 'Boiler' :
        Rel_Geraet    = 'KK1'                               # Relais Keller Boiler komplett
        Rel_Ger_DL    = 'DK1'                               # Relais für Boiler Direktladung
        Hist_Schalter = 'DK1_Hist'                          # Histerese-Schalter für Boiler Direktladung
        Rel_Ger_NL    = 'BK1'                               # Relais für Nachtladung Boiler
    else :                                                  # Abbruch , da Programmfehler unzulässiges Gerät
        raise AssertionError (' falsche Gerätedefinition "',Geraet,'" , nur "Geraet" oder "Boiler" zulässig')
    
    # Ausgabe Geraettemperatur , Prüfung , ob Histerese ein / aus / bleibt
    TextString = '- ' + Geraet + 'temperatur  aktuell ' + str(G_T_akt) + ' max ' + str(G_T_max) + ' min ' + str(G_T_min) 
    TextString = TextString + ' Histerese ' + str(G_T_hist)
    print (TextString)
    # Prüfung Plausibilität der Ladezeiten und ob für Nachtaufladung Geraet einzuschalten ist               
    NT_Lad_Geraet = Func_NT_Ladung.pruef (NT_Z_Start,NT_Z_Ende,G_Z_von,G_Z_bis,T_Z_von,T_Z_bis,T_Z_akt,G_T_akt,G_T_max)
    print (NT_Lad_Geraet)
    if   "-- Nachtladung      nicht" in NT_Lad_Geraet :   # Nachtladung nicht aktiv
        Schalt_Rel   = Rel_Geraet                         # Relais Geraet komplett abschalten
        Rel_Schalter = False                              # Relais Schalter aus
        # Entscheid , ob fǘr Direktladung Geraet eingeschaltet wird
        # Direktladung nur , wenn keine Nachtladung eingeschaltet = Histerese läuft
        # prüfen ob Histerese beginnt , endet , läuft
        Dir_Lad_Geraet = Func_Hist.pruef (G_T_akt,G_T_min,G_T_hist,Hist_Schalter)
        if   "läuft" in Dir_Lad_Geraet :          # Direktladung läuft
            Schalt_Rel   = Rel_Ger_DL             # Relais für Geraet Direktladung verwenden
            Rel_Schalter = True                   # Relais Schalter ein
            TextString = "-- Direktladung     aktiv aktuell " + str(G_T_akt) + " war gefallen unter Minimum " + str(G_T_min)
            TextString = Fore.YELLOW + TextString
        elif "ausgeschaltet" in Dir_Lad_Geraet :  # Direktladung ausgeschaltet                                                            # Direktladung läuft nicht
            TextString = "-- Direktladung     nicht aktiv"
        else :                                    # Abbruch , da Programmfehler
            raise AssertionError (' Direktladung Geraet ',Dir_Lad_Geraet) 
        print (TextString,Dir_Lad_Geraet)
        
    elif "-- Nachtladung      aktiv" in NT_Lad_Geraet :   # Nachtladung aktiv
        Schalt_Rel   = Rel_Ger_NL                         # Relais für Nachtladung Geraet verwenden
        Rel_Schalter = True                               # Relais Schalter ein
        GVS.RelTab[Hist_Schalter] = False                 # bei NT-Ladung keine Histerese
        TextString = "-- Direktladung     nicht aktiv , da Nachtaufladung"
        print (TextString)
    else :                                                # Abbruch , da Programmfehler
        raise AssertionError (' Nachtaufladung Geraet ',NT_Lad_Geraet)

    return (Schalt_Rel , Rel_Schalter)
######################################### Ende UP Geraet ############################################################