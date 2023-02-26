# shell : python3 /home/pi/skripts/prod/Entladesteuerung_V2.0.py
#         @/usr/bin/python3 /home/pi/skripts/prod.Entladesteuerung_V2.0.py

# -*- coding: utf-8 -*-   

# System- und fremde Funktionen ###########################################################
import time, sys, json, os
import logging 
from Logger import Logger

from RelaisList import RelaisList       # Funktionen zum Set / Reset von Relais
from SensorClasses import SensorList    # Funktionen zum Lesen der Temperatur Relais
from SolarLog import SolarLog           # Funktionen zum Lesen aus Solar-Log JSON Schnittstelle

# eigene externe Routinen #################################################################
import Func_Geraet         # Funktion Ausgabe Gerätetemperatur , Prüfung Nachtaufladung und ob Histerese ein / aus / bleibt 
import GVS                 # Zwischenspeicher eigene globale Variablen
# eigene externe Routinen Ende ############################################################

# Globale Sensor Liste
sensorList = SensorList()
# Globale Relais Liste
relaisList = RelaisList()
# SolarLog
solarLog = SolarLog(GVS.SolarLog_localIP)

log = Logger() 
logScreen = log.GetLogger("Screen") # nur Console Ausgaben
logMain = log.GetLogger("Main")     # Console/File Ausgaben
logSolarLog = log.GetLogger("SolarLog")

try:
    # Initialisierung des Programms und Versionsangabe
    Version = ' >> V2.0 build 2023.02.16 buster << '
    # Anzahl Verarbeitungsvorgänge
    iverarb  = 0
    # Schalter Histerese der Relais DK1 , DK2 im Keller
    GVS.RelTab['DK1_Hist'] = False    # DK1  Boiler
    GVS.RelTab['DK2_Hist'] = False    # DK2  Kessel   
    # Routine bei Neustart
    # Logsatz bei Neustart in Logdatei schreiben
    
    os.system('Clear') # Bildschirm löschen
    TextString = 'Neustart Entladesteuerung  ' + Version + '  Initialisierung :'
    logMain.log(logging.INFO, TextString)

    # Initialisierung / Reset aller Relais
    # Setzen Parameter zur Initialisierung aller Relais
    drucken      = True           # True = drucken , False = nein
    loggen       = True           # aus RelTab True = loggen , False = nein
    # Initialisierung durchführen Schalten , ggf.Ergebnis drucken , loggen
    Schalter     = False         # True = ein , False = aus
    
    relaisList.ResetAll(Schalter, drucken, loggen)  # durch Relais Liste iterieren und alle zurücksetzen

    # Endlosschleife für jeden weiteren Verarbeitungsvorgang solange bis Abbruch
    while True :
        # Initialisierung jedes einzelnen Verarbeitungsvorganges
        # Schalter initialisieren
        Raumheizung           = False
        Warmwasser            = False
        Sonstige              = False
        Tagsteuerung          = False
        boost                 = False
        drucken               = False
        loggen                = 'RelTab'   # Annahme : es wird gemäß Tabelle der Relais geloggt
                                           # abweichend möglich : True = ja , False = nein  für alle Relais   
        Schalter              = False
        
        iverarb = iverarb + 1 # Zähler Lauf

        TextString = ' START Entladesteuerung    ' + str(iverarb) + '. Lauf -----------------------------------------'
        logScreen.log(logging.INFO, TextString)
        
        if iverarb == 1 :  # Informationen zu Steuerungsparametern , Nachttarif etc. nur beim 1. Lauf
            logScreen.log(logging.INFO, "Steuerungsparameter,aktuelle Werte : (Zeiten hh:mm Temperaturen Grad Celsius)")    
        
        # aus Systembus die Werte aller Sensoren vom Typ DS18B20 auslesen , in GVS.SensTab speichern und ausdrucken
        Typ = 'DS18B20'      # Sensor Typ
        i_les_Sens     = 0   # Zähler Leseversuche ONE-Wire Bus
        i_les_Sens_max = 3   # max Anzahl Leseversuche ONE-Wire Bus
        les_wait       = 10  # Sekunden Wartezeit bei Unterbrechung ONE-Wire Bus
        Ergebnis = False     # Annahme -> shit happens
        
        while not Ergebnis and i_les_Sens < i_les_Sens_max :
            i_les_Sens = i_les_Sens + 1
            
            Ergebnis = sensorList.ReadAll(Typ)

            TextString = 'Ergebnis Auslesen aller Sensoren '
            TextString = TextString + Typ + ' ' + str(i_les_Sens) + '. Versuch '
            
            if not Ergebnis:              # Fehler --> Nachlesen
                if i_les_Sens == i_les_Sens_max :  # Nachlesen erfolglos max Anzahl Leseversuche erreicht
                    TextString = 'Auslesen aller Sensoren '
                    TextString = TextString + Typ + ' auch ' + str(i_les_Sens) + '. und letzter Versuch '
                    TextString = TextString + ' erfolglos '
                    
                    logScreen.log(logging.ERROR, TextString)
                    
                    raise AssertionError("Auslesen der Temperaturwerte fehlgeschlagen.")
                else :                             # x Mal Nachlesen , ONE-Wire Bus reset
                    TextString = 'Warnung : Auslesen aller Sensoren '
                    TextString = TextString + Typ + ' ' + str(i_les_Sens) + '. Versuch '
                    TextString = TextString + ' fehlerhaft --> Wiederholung nach ONE-Wire reset'
                    
                    logScreen.log(logging.WARNING, TextString)
                    
                    # ONE-Wire Bus unterbrechen und neuer Versuch ##############################
                    # Setzen Parameter zur Unterbrechung des ONE-Wire Bus
                    drucken    = True           # True = ja , False = nein
                    loggen     = True           # benutze RelTab True = ja , False = nein
                    RELAIS     = 'WK4'          # Relais wie in Relais-Tabelle GVS.RelTab() definiert
                    # Schaltvorgang zur Unterbrechung ONE-Wire Bus Schalten , Ergebnis drucken , loggen
                    Schalter   = True           # True = GND Ausschalten
                    
                    relais = relaisList.findRelais(RELAIS)

                    if (relais != None):
                        relais.Set(Schalter, drucken, loggen)
                    
                        time.sleep(les_wait)        # Warten vor wieder Einschalten !
                        Schalter   = False          # False = GND wieder Einschalten
                        relais.Set(RELAIS, Schalter, drucken, loggen)))
                    
                    time.sleep (les_wait)       # Warten vor dem nächsten Auslesen !
                    # Ende ONE-Wire Bus zurücksetzen und neuer Versuch #########################
            # durch die Sensor Liste gehen und die Ergebnisse (Temperatur, Fehler) ausdrucken
            sensorList.PrintResults(Typ)
               
        # Informationen aufbereiten , Parameter setzen , prüfen , Istwerte ermitteln       
        # JSON Datei mit Parametern einlesen
        with open('/home/pi/skripts/prod/Parameter.json') as f:
            config_raw = f.read()
        # Konvertieren der gelesenen bytes in einen JSON string
        config = json.loads(config_raw)
        
        # Heizung / Warmwasser ein- oder ausgeschaltet ?        
        if config['Parameter']['Raumheizung'] == 'ein' : Raumheizung = True
        if config['Parameter']['Warmwasser']  == 'ein' : Warmwasser  = True
        if config['Parameter']['Sonstige']    == 'ein' : Sonstige    = True
        
        # Tagsteuerung von bis
        DTvon = config['Parameter']['Tagsteuerung']['DTvon']
        DTbis = config['Parameter']['Tagsteuerung']['DTbis']
        #  aktuelle Tageszeit
        DTakt = time.strftime("%H:%M")
        # Beginn und Ende der Niedertarifzeit während der Nacht
        NT_Zeit_Start = config['Parameter']['NT_Zeit']['Start']
        NT_Zeit_Ende  = config['Parameter']['NT_Zeit']['Ende']
        # Raumtemperatur , aktuell, min , max
        RTakt = GVS.SensTab.get('Raum' + '_Tmp')
        RTmin = config['Parameter']['Raumtemperatur']['RTmin']
        RTmax = config['Parameter']['Raumtemperatur']['RTmax']
        # Boilertemperatur  aktuell , min , max , hist , Nachtladung
        BTakt = GVS.SensTab.get('Boiler' + '_Tmp')
        BTmin  = config['Parameter']['Boilertemperatur']['BTmin']
        BTmax  = config['Parameter']['Boilertemperatur']['BTmax']
        BThist = config['Parameter']['Boilertemperatur']['BThist']
        BNvon  = config['Parameter']['NT_Aufl_Boiler']['BNvon']
        BNbis  = config['Parameter']['NT_Aufl_Boiler']['BNbis']
        # Vorlauftemperatur , aktuell , max
        VTakt = GVS.SensTab.get('Vorlauf' + '_Tmp')
        VTmax = config['Parameter']['Vorlauftemperatur']['VTmax']
        # Kesseltemperatur aktuell , min , max , boosttemperatur , boostzeit , Nachtladung
        KTakt = GVS.SensTab.get('Kessel' + '_Tmp')
        KTmin   = config['Parameter']['Kesseltemperatur']['KTmin']
        KTmax   = config['Parameter']['Kesseltemperatur']['KTmax']
        KThist  = config['Parameter']['Kesseltemperatur']['KThist']
        KTboost = config['Parameter']['Kesseltemperatur']['KTboost']
        KNvon   = config['Parameter']['NT_Aufl_Kessel']['KNvon']
        KNbis   = config['Parameter']['NT_Aufl_Kessel']['KNbis']
        # Beginn und Ende boost
        BZvon = config['Parameter']['boostZeit']['von']
        BZbis = config['Parameter']['boostZeit']['bis']
        # min erforderliche PV-Erzeugung
        PVmin = config['Parameter']['Erzeugung']['PVmin']
        # Wartezeit bis zum nächsten Lauf
        wait = config['Parameter']['Zyklus']['Sekunden']
        NachtFaktor = config['Parameter']['Zyklus']['NachtFak']
        
        if iverarb == 1 :  # Informationen zu Steuerungsparametern , Nachttarif etc. nur beim 1. Lauf
            logScreen.log(logging.INFO, 19 * ' ' + f'(Zyklus Tag {wait} Nachtfaktor {NachtFaktor} Zyklus Nacht {wait * NachtFaktor}')
        
        # Beginn Verarbeitung #########################################################################
        # Ausgabe Istwerte bei jedem Lauf unabhängig Raumheizung oder Warmwasserbereitung
        
        # Fotovoltaik-Informationen lesen und ausgeben          # lokale IP des Solar-Log aus GVS 
                
        if not solarLog.Read():                              # Solar-log Fehler beim Lesen Warnung ausgeben
            SoLo_Text = 'Photovoltaik Warnung : ' + solarLog.lastError
            SoLo_Bezug     = 0
            Solo_Erzeugung = 0                                  # Erzeugung und Bezug mit 0 angenommen
            logScreen.log(logging.WARNING, SoLo_Text)
            logScreen.log(logging.WARNING, 20 * ' ' + 'Erzeugung und Bezug für weitere Verarbeitung mit 0 angenommen !')
        else :                                                  # Solar-log Bezug und Erzeugung ermitteln
            GVS.SolarLog_Erzeugung = solarLog.Erzeugung # Abwärtskompatibilität
            GVS.SolarLog_Verbrauch = solarLog.Verbrauch

            SoLo_Bezug = solarLog.Bezug
            Solo_Erzeugung = solarLog.Erzeugung

            SoLo_Text = "Verbrauch " + str(GVS.SolarLog_Verbrauch)
            logSolarLog.log(logging.ERROR, SoLo_Text)
            logSolarLog.log(logging.WARNING, " Erzeugung " + str(GVS.SolarLog_Erzeugung))
            SoLo_Text = SoLo_Text + " Erzeugung " + str(GVS.SolarLog_Erzeugung)

            if solarLog.Bezug >= 0 :
                logSolarLog.log(logging.INFO, " Einspeisung " + str(solarLog.Bezug) + ' KW ')
            else :
               logSolarLog.log(logging.ERROR, " Bezug " + str(solarLog.Bezug) + ' KW ')

            logSolarLog.log(logging.INFO, SoLo_Text + f' Tagbetrieb erst ab PVmin {PVmin}')
        
        # Prüfung , ob Raumheizung pausiert                       # Pause von ... bis ...  ?
        # Raumheizung pausieren , wenn PV-Überschuß nicht ausreichend und
        # Ende Tagzeit bis Beginn Nachttarif oder Ende Nachttarif bis Beginn Tagzeit
        if  Raumheizung \
            and SoLo_Bezug < PVmin \
            and (DTakt > DTbis and DTakt < NT_Zeit_Start \
            or   DTakt > NT_Zeit_Ende and DTakt < DTvon) :  
            Raumheizung = False                           # Raumheizung pausiert
            if  DTakt > NT_Zeit_Ende and DTakt < DTvon : 
                TextString = ' von ' + NT_Zeit_Ende + ' bis ' + DTvon
            else :
                TextString = ' von ' + DTbis + ' bis ' + NT_Zeit_Start
            TextString = 'Raumheizung         pausiert' + TextString
            TextString = TextString + ' , PV-Überschuß nicht ausreichend , Steuerung ausgeschaltet'
            logScreen.log(logging.WARNING, TextString)
                
        # Ausgabe Istwerte nur relevant bei aktiver Raumheizung
        if Raumheizung:
            # Entscheid , ob Tagbetrieb oder Nachtabsenkung , entsprechende Ausgabe
            TextString = 'Raumheizung         eingeschaltet '
            # Tagbetrieb nur zwischen 7 und 21 Uhr zulässig !
            if DTvon >=  DTbis or DTvon < '07:00' or DTbis > '21:00' :
                TextString = 'weitere Verarbeitung nicht möglich , '
                if not DTbis > DTvon:
                    TextString = TextString + 'Tagbetrieb "bis" muß größer sein als "von"'
                else :
                    TextString = TextString + 'Tagbetrieb nur von 7 bis 21 Uhr'
                TextString = TextString + '\n'   # neue Zeile
                TextString = TextString + 20 * ' ' + 'Parameter korrigieren in : /home/pi/skripts/prod/Parameter.json'
                raise AssertionError (TextString)
            
            if SoLo_Bezug > PVmin:                      # ausreichender PV-Überschuß --> immer Tagsteuerung
                TextString = TextString + ' (Tagbetrieb , da ausreichend PV-Überschuß)'
                Tagsteuerung = True
            else :                                       # wenn kein ausreichender PV-Überschuß
                if (DTakt >= DTvon and DTakt <= DTbis) : # Tagsteuerung während der Tagzeit
                    TextString = TextString + "(Tagbetrieb von " + DTvon + " bis " + DTbis
                    Tagsteuerung = True
                else :                                   # ansonsten Nachtabsenkung                                           
                    TextString = TextString + "(Nachtabsenkung von " + DTbis + " bis " + DTvon
                    Tagsteuerung = False
                TextString = TextString + ' Nachttarif (NT) ' + NT_Zeit_Start + ' bis ' + NT_Zeit_Ende + ')'
            logScreen.log(logging.INFO, TextString)
            # Ausnahmen bei Tagsteuerung --> Umschalten auf Nachtabsenkung
            if Tagsteuerung :
                TextString = ''
                if Tagsteuerung and GVS.SolarLog_Erzeugung < PVmin and not 'Fehler' in SoLo_Text :
                    TextString = 'PV-Erzeugung nicht ausreichend (min ' + str(PVmin) + ' erforderlich)'
                if  Tagsteuerung and VTakt > VTmax :
                    TextString = 'Vorlauftemperatur ' + str(VTakt) + ' über Maximum ' + str(VTmax)
                if  Tagsteuerung and KTakt < KTmin + KThist :
                    TextString = 'Kesseltemperatur ' + str(KTakt) + ' unter ' + str(KTmin + KThist) + ' (min + hist)'
                if TextString != '' :
                    Tagsteuerung = False
                    TextString = "- Tagbetrieb        aber Nachtabsenkung , da " + TextString
                    logScreen.log(logging.WARNING,TextString) 
            # Ausnahmen bei Nachtabsenkung --> Umschalten auf Tagsteuerung
            else :
                TextString = ''
                if RTakt < RTmin  :  # --> Tagsteuerung immer aktiv , wenn ...
                    TextString = "aktuelle Raumtemperatur" + str(RTakt) + 'unter Minimum' + str(RTmin)
                if TextString != '' :
                    Tagsteuerung = True
                    TextString = "- Nachtabsenkung    aber Tagbetrieb , da " + TextString
                    logScreen.log(logging.WARNING, TextString) 
            
            # Ausgabe Raumtemperatur 
            print ("- Raumtemperatur    aktuell",RTakt,"max",RTmax,'min',RTmin)        

            # Ausgabe Kesseltemperatur , Prüfung Nachtaufladung und ob Histerese ein / aus / bleibt #########################
            Ergebnis = Func_Geraet.pruef('Kessel', NT_Zeit_Start, NT_Zeit_Ende, KNvon, KNbis, DTvon, DTbis,
                                DTakt, KTakt, KTmin, KTmax, KThist)
            
            Rel_NameKessel    = Ergebnis.pop(0)   # 1. Parameter des Ergebnisses : betreffendes Relais
            Rel_SchKessel     = Ergebnis.pop(0)   # 2. Parameter des Ergebnisses : betreffender Schalter
            e                 = Ergebnis.pop(0)   # 3. Parameter des Ergebnisses : Fehlermeldung bei Abbruch

            if 'Fehler' in e :                    # Abbruch bei Programmfehler
                raise AssertionError (e)
            else :                                # Ausgabe Temperatur , Direkt- und Nachtladung
                logScreen.log(logging.INFO, e)

            # Ende Ausgabe Kesseltemperatur #################################################################################

            # Ausgabe Vorlauftemperatur
            if VTakt > VTmax :
                logScreen.log(logging.INFO, f'- Vorlauftemperatur aktuell {VTakt} max {VTmax} überschritten')
            else :
                logScreen.log(logging.INFO, f'- Vorlauftemperatur aktuell {VTakt} max {VTmax}')
            
            # Entscheid, ob boost eingeschaltet wird
            if Tagsteuerung :
                boost = True
            else :
                boost = False
                logScreen.log(logging.INFO, '- boost             nicht aktiv bei Nachtabsenkung')
            if SoLo_Bezug < 0  and boost :
                boost = False
                logScreen.log(logging.INFO,f'- boost             nicht aktiv , kein PV-Überschuss (Bezug {SoLo_Bezug})')
            if KTakt < KTboost and boost :
                boost = False
                logScreen.log(logging.INFO,f'- boost             nicht aktiv Kesseltemperatur unter {KTboost}')
            if VTakt > VTmax   and boost :
                boost = False
                logScreen.log(logging.INFO,f'- boost             nicht aktiv Vorlauftemperatur größer {VTmax}')
            if RTakt > RTmax   and boost :
                boost = False
                logScreen.log(logging.INFO,f'- boost             nicht aktiv Raumtemperatur größer {RTmax}')
            if DTakt < BZvon   and boost :
                boost = False
                logScreen.log(logging.INFO,f'- boost             nicht aktiv erst ab {BZvon} verfügbar')
            if DTakt > BZbis   and boost :
                boost = FalseSchalter     = True
                logScreen.log(logging.INFO,f'- boost             nicht aktiv nur bis {BZbis} verfügbar')
            if boost :
                logScreen.log(logging.INFO,f'- boost             aktiv von {BZvon} bis {BZbis} bei {KTboost} Einspeisung {SoLo_Bezug}')
            else :
                if RTakt < RTmin :
                    boost = True
                    logScreen.log(logging.INFO, f'- boost             aktiv weil Raumtemperatur {RTakt} unter Minimum {RTmin}!')
        else :
            if not 'pausiert' in TextString :
                print ('Raumheizung         Steuerung ausgeschaltet')
            # Relais für Raumheizung und Kessel :  werden bzw. bleiben ausgeschaltet !
            Tagsteuerung          = False
            boost                 = False
        
        # Ausgabe Istwerte nur relevant für Warmwasserbereitung
        if Warmwasser :
            TextString = 'Warmwasserbereitung eingeschaltet '
            TextString = TextString + f'(Nachttarif (NT) {NT_Zeit_Start} bis {NT_Zeit_Ende}'
            logScreen.log(logging.INFO, TextString)
            
            # Ausgabe Boilertemperatur , Prüfung Nachtaufladung und ob Histerese ein / aus / bleibt #########################

            Ergebnis = Func_Geraet.pruef('Boiler',NT_Zeit_Start,NT_Zeit_Ende,BNvon,BNbis,DTvon,DTbis,DTakt,BTakt,BTmin,BTmax,BThist)
            
            Rel_NameBoiler    = Ergebnis.pop(0)   # 1. Parameter des Ergebnisses : betreffendes Relais
            Rel_SchBoiler     = Ergebnis.pop(0)   # 2. Parameter des Ergebnisses : betreffender Schalter
            e                 = Ergebnis.pop(0)   # 3. Parameter des Ergebnisses : Fehlermeldung bei Abbruch

            if 'Fehler' in e :                    # Abbruch bei Programmfehler
                raise AssertionError (e)
            else :                                # Ausgabe Temperatur , Direkt- und Nachtladung
                logScreen.log(logging.INFO, e)

           # Ende Ausgabe Boilertemperatur #################################################################################
        
        else :
            logScreen.log(logging.INFO, 'Warmwasserbereitung Steuerung ausgeschaltet')
        
        # Abbruch , wenn weder Raumheizung noch Warmwasser eingeschaltet
        if not (Raumheizung or Warmwasser or Sonstige) :
            TextString = 'weitere Verarbeitung nicht sinnvoll , weder Raumheizung noch Warmwasser eingeschaltet'
            TextString = TextString + '\n'   # neue Zeile
            TextString = TextString + 20 * ' ' + 'Parameter korrigieren in : /home/pi/skripts/prod/Parameter.json'
            raise AssertionError (TextString)
                
        # Beginn Relais - Schaltvorgänge ###########################################################################
        #  Aktionen Kessel und Tagsteuerung nur , wenn Raumheizung eingeschaltet ist !
        TextString = 'Schaltvorgänge  :   '  
        TextString = TextString + "(Hintergrund rot->aus,grün->ein  Schrift weiß->unverändert,schwarz->geschaltet)"
        logScreen.log(logging.INFO, TextString) 
        
        if Raumheizung:            
            TextString = '- Raumheizung   :'
            logScreen.log(logging.INFO, TextString)
            
            # Setzen Parameter zur Schaltung von Relais WK1 für die Funktion Tag-/Nachtbetrieb
            RELAIS       = 'WK1'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            # für Tagbetrieb Tagsteuerung=True=einschalten , für Nachtbetrieb Tagsteuerung=False=ausschalten
            # Schaltvorgang durchführen
            relais = relaisList.findRelais(RELAIS)
            if not relais is None: 
                relais.Set(Tagsteuerung, drucken, loggen))
          
            # Setzen Parameter zur Schaltung von Relais WK2 für die Funktion boost
            RELAIS       = 'WK2'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            # boost=True=einschalten , boost=False= ausschalten
            # Schaltvorgang durchführen
            relais = relaisList.findRelais(RELAIS)
            if not relais is None:
                relais.Set(boost, drucken, loggen)            
                        
            # Schaltung Relais K2 für den Kessel im Keller
            # Parameter bereits gesetzt oben durch Funktion Func_Geraet.pruef
            RELAIS       = Rel_NameKessel   # Relais wie in Relais-Tabelle definiert
            Schalter     = Rel_SchKessel    # True = ein , False = aus
            drucken      = True             # True = ja , False = nein
            # Schaltvorgang durchführen            
            relais = relaisList.findRelais(RELAIS)
            if not relais is None:
                relais.Set(Schalter, drucken, loggen)
            
        #  keine Raumheizung --> alle Relais ausschalten , die davon betroffen sind !           
        else :
            TextString = '- Raumheizung       und zugehörige Relais WK1,WK2,KK2<HK2,DK2> ausgeschaltet' 
            logScreen(logging.WARNING, TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            RELAIS = 'WK1'
            relais = relaisList.findRelais(RELAIS)
            if not relais is None:
                relais.Set(Schalter, drucken, loggen)
            RELAIS = 'WK2'
            relais = relaisList.findRelais(RELAIS)
            if not relais is None:
                relais.Set(Schalter, drucken, loggen)
            RELAIS = 'KK2'  # KK2 = HK2 = DK2 , gleiches Relais
            relais = relaisList.findRelais(RELAIS)
            if not relais is None: 
                relais.Set(Schalter, drucken, loggen)

        #  Aktionen Boiler nur , wenn Warmwasser eingeschaltet ist !
        if Warmwasser :
            logScreen.log(logging.INFO, '- Warmwasser    :')
            # Schaltung Relais K1 für den Boiler im Keller
            # Parameter bereits gesetzt oben durch Funktion Func_Geraet.pruef
            RELAIS       = Rel_NameBoiler   # Relais wie in Relais-Tabelle definiert
            Schalter     = Rel_SchBoiler    # True = ein , False = aus
            drucken      = True             # True = ja , False = nein
            # Schaltvorgang durchführen
            relais = relaisList.findRelais(RELAIS)
            if not relais is None: 
                relais.Set(Schalter, drucken, loggen)
                    
        #  Keine Warmwasserbereitung -->  Relais Boiler ausschalten          
        else :  
            logScreen.log(logging.WARNING, TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            RELAIS = 'KK1'   # KK1 = BK1 = DK1 , gleiches Relais
            relais = relaisList.findRelais(RELAIS)
            if not relais is None: 
                relais.Set(Schalter, drucken, loggen)
 
        # Sonstige Schaltvorgänge
        if Sonstige :
            logScreen.log(logging.INFO, '- Sonstige      :')
            
            # Setzen Parameter zum Pingen von Relais WK3 für TFA 3035 pingen
            RELAIS       = 'WK3'            # Relais wie in Relais-Tabelle definiert
            drucken      = False            # True = ja , False = nein
            Schalter     = True             # Ping ein
            # Schaltvorgang durchführen
            relais = relaisList.findRelais(RELAIS)
            if not relais is None: 
                relais.Set(Schalter, drucken, loggen)                
                Schalter     = False            # Ping aus
                # Schaltvorgang durchführen
                relais.Set(Schalter, drucken, loggen)
                logScreen.log(logging.WARNING, f' Relais {RELAIS} TFA 3035 angepingt ohne weitere Aktion')            
            
            # Setzen Parameter zum Schalten von Relais GK1 Garten
            RELAIS       = 'GK1'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            PVmin        = 0.5 * PVmin
            if SoLo_Bezug >=  PVmin :       # nur einschalten , wenn ausreichender PV-Ertrag
                Schalter     = True
                TextString   = f'(Einspeisung für Garten ausreichend {SoLo_Bezug} >= 1/2 PVmin {PVmin})'
            else :
                Schalter     = False
                if SoLo_Bezug >= 0 :
                    TextString  = f'(Einspeisung für Garten nicht ausreichend {SoLo_Bezug} < 1/2 PVmin {PVmin})'
                else :
                    TextString  = f'(Einspeisung für Garten nicht ausreichend , da Bezug negativ {SoLo_Bezug})'
            # Schaltvorgang durchführen
            relais = relaisList.findRelais(RELAIS)
            if not relais is None: 
                relais.Set(Schalter, drucken, loggen)
            
            logScreen.log(logging.INFO, TextString)
            
        #  keine Sonstige --> alle Relais ausschalten , die davon betroffen sind !   
        else :
            logScreen.log(logging.WARNING, 'Sonstige            und zugehörige Relais WK3,GK1 ausgeschaltet')  
            print (TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            ARRAY_RELAIS = ['WK3', 'GK1']   # ping-Relais und Garten Reais
            for relaisName in ARRAY_RELAIS:
                relais = relaisList.findRelais(RELAIS)
                if not relais is None: 
                    relais.Set(Schalter, drucken, loggen)
        # Ende Schaltvorgänge #######################################################################################
        if not Tagsteuerung : wait = wait * NachtFaktor # in der Nacht verlängerter Zyklus
        if iverarb == 1   : wait = wait / 2             # beim 1. Lauf nur 1/2 Zeit warten
        TextString = f' ENDE Entladesteuerung     {iverarb + 1}. Lauf beginnt in {wait} Sekunden ----------------'
        logScreen.log(logging.INFO, TextString)
        
        # Ende Endlosschleife nächster Lauf zyklisch nach x Sekunden
        logScreen.log(logging.INFO, "")
        time.sleep(wait)
    # while(true) Block Ende
    END_TEXT = ''
except KeyboardInterrupt as e :
    # Programm beendet mit CTRL+C oder Strg+C
    END_TEXT   = 'ENDE Entladesteuerung ' + Version
    logMain.log(logging.INFO, END_TEXT)
    END_TEXT1  = 'mit KeyboardInterrupt (CTRL+C oder Strg+C)'
    logMain.log(logging.INFO, END_TEXT1)
except AssertionError as e :
    # Programm ABBRUCH mit AssertionError
    END_TEXT   = 'ABBRUCH Entladesteuerung ' + Version
    END_TEXT1  = 'mit AssertionError : '
    END_TEXT2  = str(e)        
except Exception as e :
    # Programm ABBRUCH mit Exception
    END_TEXT   = 'ABBRUCH Entladesteuerung ' + Version
    END_TEXT1  = 'mit Exception : '
    END_TEXT2  = str(e)
finally :
    logScreen.log(logging.INFO, "")
    # Das Programm wird hier beendet
    if END_TEXT == '':                                      # ordnungsgemäß beendet
        logScreen.log(logging.INFO, '---> Programm fehlerfrei beendet und')
    else:                                                   # Abbruch mit Assertion oder Exception
        logMain.log(logging.INFO, END_TEXT)                 # 1. Zeile Loggen und Drucken
        logFile = Logger().GetLogger("Log")
        logFile.log(logging.ERROR, END_TEXT1)               # 2. Zeile Loggen , nicht Drucken
        logFile.log(logging.ERROR, END_TEXT2)               # 3. Zeile Loggen , nicht Drucken       
    # Initialisierung / Reset aller Relais
    # Setzen Parameter zur Initialisierung aller Relais
    drucken      = True           # True = ja , False = nein
    loggen       = True           # True = ja , False = nein
    # Initialisierung durchführen Reset , ggf.Ergebnis drucken , loggen
    Schalter     = False         # True = ein , False = aus
    relaisList.ResetAll(Schalter, drucken, loggen)

#   sys.exit(0)  # wenn kein Fehler in die Console geschrieben werden soll
