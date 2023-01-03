# shell : python3 /home/pi/skripts/prod/Entladesteuerung.py
#         @/usr/bin/python3 /home/pi/skripts/prod.Entladesteuerung.py

# -*- coding: utf-8 -*-   

# System- und fremde Funktionen
import time , sys , RPi.GPIO as GPIO  , json

from colorama import init , Fore , Style , Back
                    # init(autoreset=True) Farbe gilt nur je Printposition
                    # init()               Farbe gilt bis Programmende
                    #Farben :
                    #Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Style: DIM, NORMAL, BRIGHT, RESET_ALL
init(autoreset=True)

# eigene Routinen
import Func_Temp_Sens      # Funktion zum Abfragen der Temperatursensoren
import Func_Relais         # Funktion zum Schalten der Relais
import Func_Solar_Log      # Funktion zum Lesen aus Solar-Log JSON
import Func_NT_Ladung      # Funktion zur Prüfung , ob Nachttarifladung eines Gerätes möglich
import Func_Hist           # Funktion zur Prüfung der Histerese
import GVS                 # Zwischenspeicher eigene globale Variablen



try:
    # Initialisierung des Programms
    # Fehlertext bei Abbruch
    END_TEXT = ''
    # Anzahl Verarbeitungsvorgänge
    iverarb  = 0
    # Schalter Histerese der Relais DK1 , DK2 im Keller
    GVS.RelTab['DK1_Hist'] = False    # DK1  Boiler
    GVS.RelTab['DK2_Hist'] = False    # DK2  Kessel
    
    # Endlosschleife für jeden Verarbeitungsvorgang solange bis Abbruch
    while True :
        # Initialisierung jedes einzelnen Verarbeitungsvorganges
        # Schalter initialisieren
        Raumheizung           = False
        Warmwasser            = False
        Sonstige              = False
        Tagsteuerung          = False
        boost                 = False
        Direktladung_Boiler   = False
        NT_Ladung_Boiler      = False
        drucken               = False
        loggen                = False
        Schalter              = False
        
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
        # Sensor 28-0309977914a4
        sensorRT = Func_Temp_Sens.sensorRT
        RTakt = Func_Temp_Sens.readTempLines(sensorRT)[0]
        RTmin = config['Parameter']['Raumtemperatur']['RTmin']
        RTmax = config['Parameter']['Raumtemperatur']['RTmax']
        # Boilertemperatur  aktuell , min , max , hist , Nachtladung
        # Sensor 28-0316a27937aa
        sensorBT = Func_Temp_Sens.sensorBT
        BTakt  =   Func_Temp_Sens.readTempLines(sensorBT)[0]
        BTmin  = config['Parameter']['Boilertemperatur']['BTmin']
        BTmax  = config['Parameter']['Boilertemperatur']['BTmax']
        BThist = config['Parameter']['Boilertemperatur']['BThist']
        BNvon  = config['Parameter']['NT_Aufl_Boiler']['BNvon']
        BNbis  = config['Parameter']['NT_Aufl_Boiler']['BNbis']
        # Vorlauftemperatur , aktuell , max
        # Sensor 28-030997790e32
        sensorVT = Func_Temp_Sens.sensorVT
        VTakt = Func_Temp_Sens.readTempLines(sensorVT)[0]
        VTmax = config['Parameter']['Vorlauftemperatur']['VTmax']
        # Kesseltemperatur aktuell , min , max , boosttemperatur , boostzeit , Nachtladung
        # Sensor 28-030997790a01
        sensorKT = Func_Temp_Sens.sensorKT
        KTakt   = Func_Temp_Sens.readTempLines(sensorKT)[0]
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
        # Fotovoltaik-Informationen
        #localIP = '169.254.34.32'                                                # lokale IP des Solar-Log aus GVS
        SoLo_Text = Func_Solar_Log.Lesen(GVS.SolarLog_localIP)                    # Solar-log JSON lesen
        SoLo_Bezug = (round((GVS.SolarLog_Erzeugung - GVS.SolarLog_Verbrauch),2)) # Solar-log Bezug ermitteln
        Solo_Erzeugung = round(GVS.SolarLog_Erzeugung,2)                          # Solar-log Erzeugung ermitteln
                
        # Beginn Verarbeitung #########################################################################
        
        iverarb = iverarb + 1 # Zähler Lauf
        
        print ()
        TextString = ' START Entladesteuerung    ' + str(iverarb) + '. Lauf -----------------------------------------'
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
        print (Fore.GREEN + TextString)
                
        if iverarb == 1 :  # Informationen zu Steuerungsparametern , Nachttarif nur beim 1. Lauf
            print ("Steuerungsparameter,aktuelle Werte : (Zeiten hh:mm , Temperaturen Grad Celsius)")        
        
        # Ausgabe Istwerte bei jedem Lauf unabhängig Raumheizung oder Warmwasserbereitung
        print (SoLo_Text,'PVmin =',PVmin)                       # Text des Solar-Log Drucken mit Angabe PVmin
        if GVS.SolarLog_Erzeugung <= 0 and GVS.SolarLog_Verbrauch <= 0 :
            print (Fore.YELLOW + '                    alle Werte mit o angenommen für weitere Verarbeitung')  # Zusatz bei Lesefehlern
        
        # Ausgabe Istwerte nur relevant für Raumheizung
        if Raumheizung :
            
            # Entscheid , ob Tagsteuerung oder Nachtabsenkung , entsprechende Ausgabe
            TextString = 'Raumheizung         eingeschaltet '
            # nur Tagbetrieb von 7 bis 21 Uhr zulässig !
            if DTvon >=  DTbis or DTvon < '07:00' or DTbis > '21:00' :
                TextString = 'weitere Verarbeitung nicht möglich , '
                if not DTbis > DTvon :
                    TextString = TextString + 'Tagsteuerung "bis" muß größer sein als "von"'
                else :
                    TextString = TextString + 'Tagsteuerung nur von 7 bis 21 Uhr'
                TextString = TextString + '\n'   # neue Zeile
                TextString = TextString + 20 * ' ' + 'Parameter korrigieren in : /home/pi/skripts/prod/Parameter.json'
                raise AssertionError (TextString)
                
            if DTakt >= DTvon and DTakt <= DTbis :   # grundsätzlich Tagsteuerung
                TextString = TextString + "(Tagbetrieb von " + DTvon + " bis " + DTbis
                Tagsteuerung = True
            else :                                   # grundsätzlich Nachtabsenkung                                           
                TextString = TextString + "(Nachtabsenkung von " + DTbis + " bis " + DTvon
                Tagsteuerung = False
            TextString = TextString + ' Nachttarif (NT) ' + NT_Zeit_Start + ' bis ' + NT_Zeit_Ende + ')'    
            print (TextString)
            # Ausnahmen bei Tagsteuerung --> Umschalten auf Nachtabsenkung
            if Tagsteuerung :
                TextString = ''
                if Tagsteuerung and GVS.SolarLog_Erzeugung < PVmin :
                    TextString = 'PV-Erzeugung nicht ausreichend (min ' + str(PVmin) + ' )'
                if  Tagsteuerung and VTakt > VTmax :
                    TextString = 'Vorlauftemperatur ' + str(VTakt) + ' über Maximum ' + str(VTmax)
                if  Tagsteuerung and KTakt < KTmin + KThist :
                    TextString = 'Kesseltemperatur ' + str(KTakt) + ' unter ' + str(KTmin + KThist) + ' (min + hist)'
                if TextString != '' :
                    Tagsteuerung = False
                    TextString = Fore.YELLOW + "- Tagbetrieb        aber Nachtabsenkung , da " + TextString
                    print (TextString) 
            # Ausnahmen bei Nachtabsenkung --> Umschalten auf Tagsteuerung
            else :
                TextString = ''
                if RTakt < RTmin  :  # --> Tagsteuerung immer aktiv , wenn ...
                    TextString = "aktuelle Raumtemperatur" + str(RTakt) + 'unter Minimum' + str(RTmin)
                if TextString != '' :
                    Tagsteuerung = True
                    TextString = Fore.YELLOW + "- Nachtabsenkung    aber Tagbetrieb , da " + TextString
                    print (TextString) 
            
            # Ausgabe Raumtemperatur 
            print ("- Raumtemperatur    aktuell",RTakt,"max",RTmax,'min',RTmin)
            
###################################### Beginn Hauptprogramm neu ############################################################# 
            # Ausgabe Kesseltemperatur , Prüfung , ob Histerese ein / aus / bleibt
            TextString = "- Kesseltemperatur  aktuell " + str(KTakt) + " max "+ str(KTmax)+ " min " + str(KTmin) 
            TextString = TextString + ' Histerese ' + str(KThist)
            print (TextString)
            # Prüfung Plausibilität der Ladezeiten und ob für Nachtaufladung Kessel einzuschalten ist               
            NT_Lad_Kessel = Func_NT_Ladung.pruef (NT_Zeit_Start,NT_Zeit_Ende,KNvon,KNbis,DTvon,DTbis,DTakt,KTakt,KTmax)
            print (NT_Lad_Kessel)
            if   "-- Nachtladung      nicht" in NT_Lad_Kessel :   # Nachtladung nicht aktiv
                K2_Relais   = 'KK2'                               # Relais Kessel komplett abschalten
                K2_Schalter = False                               # Relais Schalter aus
                # Entscheid , ob fǘr Direktladung Kessel eingeschaltet wird
                # Direktladung nur , wenn keine Nachtladung eingeschaltet = Histerese läuft
                # prüfen ob Histerese beginnt , endet , läuft
                Hist_Schalter = 'DK2_Hist'         # Histerese-Schalter für Kessel Direktladung
                Dir_Lad_Kessel = Func_Hist.pruef (KTakt,KTmin,KThist,Hist_Schalter)
                if   "läuft" in Dir_Lad_Kessel :          # Direktladung läuft
                    K2_Relais   = 'DK2'                   # Relais für Kessel Direktladung verwenden
                    K2_Schalter = True                    # Relais Schalter ein
                    TextString = "-- Direktladung     aktiv aktuell " + str(KTakt) + " war gefallen unter Minimum " + str(KTmin)
                    TextString = Fore.YELLOW + TextString
                elif "ausgeschaltet" in Dir_Lad_Kessel :  # Direktladung ausgeschaltet                                                            # Direktladung läuft nicht
                    TextString = "-- Direktladung     nicht aktiv"
                else :                                    # Abbruch , da Programmfehler
                    raise AssertionError (' Direktladung Kessel ',Dir_Lad_Kessel) 
                print (TextString,Dir_Lad_Kessel)
                
            elif "-- Nachtladung      aktiv" in NT_Lad_Kessel :   # Nachtladung aktiv
                K2_Relais   = 'HK2'                               # Relais für Nachtladung Kessel verwenden
                K2_Schalter = True                                # Relais Schalter ein
                GVS.RelTab[Hist_Schalter] = False                 # bei NT-Ladung keine Histerese
                TextString = "-- Direktladung     nicht aktiv , da Nachtaufladung"
                print (TextString)
            else :                                                # Abbruch , da Programmfehler
                raise AssertionError (' Nachtaufladung Kessel ',NT_Lad_Kessel)
            
###################################### Ende Hauptprogramm neu ################################################################            
 
            # Ausgabe Vorlauftemperatur
            if VTakt > VTmax :
                print ("- Vorlauftemperatur aktuell",VTakt,"max",VTmax,'überschritten')
            else :
                print ("- Vorlauftemperatur aktuell",VTakt,"max",VTmax)
            
            # Entscheid , ob boost eingeschaltet wird
            if Tagsteuerung :
                boost = True
            else :
                boost = False
                print ('- boost             nicht aktiv bei Nachtabsenkung')
            if SoLo_Bezug < 0  and boost :
                boost = False
                print ('- boost             nicht aktiv , kein PV-Überschuss (Bezug ' , SoLo_Bezug, ')')
            if KTakt < KTboost and boost :
                boost = False
                print ('- boost             nicht aktiv Kesseltemperatur unter ',KTboost)
            if VTakt > VTmax   and boost :
                boost = False
                print ('- boost             nicht aktiv Vorlauftemperatur größer ',VTmax)
            if RTakt > RTmax   and boost :
                boost = False
                print ('- boost             nicht aktiv Raumtemperatur größer ',RTmax)
            if DTakt < BZvon   and boost :
                boost = False
                print ('- boost             nicht aktiv erst ab ',BZvon,' verfügbar')
            if DTakt > BZbis   and boost :
                boost = FalseSchalter     = True
                print ('- boost             nicht aktiv nur bis ',BZbis,' verfügbar')
            if boost :
                print ("- boost             aktiv von ",BZvon,' bis ',BZbis,' bei ',KTboost,' Einspeisung ',SoLo_Bezug)
            else :
                if RTakt < RTmin :
                    boost = True
                    print (Fore.RED +
                       "- boost             aktiv weil Raumtemperatur " + str(RTakt) + " unter Minimum " + str(RTmin) + '!')
        else :
            print ('Raumheizung         Steuerung ausgeschaltet')
            # Relais für Raumheizung und Kessel :  werden bzw. bleiben ausgeschaltet !
            Tagsteuerung          = False
            boost                 = False
        
        # Ausgabe Istwerte nur relevant für Warmwasserbereitung
        if Warmwasser :
            TextString = 'Warmwasserbereitung eingeschaltet '
            TextString = TextString + '(Nachttarif (NT) ' + NT_Zeit_Start + ' bis ' + NT_Zeit_Ende + ')'
            print (TextString) 
            print ("- Boilertemperatur  aktuell",BTakt,"max",BTmax,"min",BTmin,'hist ',BThist)

            # Prüfung , ob Nachtaufladung Boiler oder alternativ Direktladung einzuschalten ist
            # Entscheid , ob fǘr Nachtaufladung Boiler eingeschaltet wird
            # Prüfung Plausibilität der Ladezeiten                
            NT_Zeit_Boiler = Func_NT_Ladung.pruef (NT_Zeit_Start,NT_Zeit_Ende,BNvon,BNbis,DTvon,DTbis,DTakt,BTakt,BTmax)
            if NT_Zeit_Boiler not in ['ein','aus'] :     # bei Intervall-Fehler Abbruch
                raise AssertionError (' Nachtaufladung Kessel ',NT_Zeit_Boiler)    
            # Nachtaufladung einschalten ?         
            if NT_Zeit_Boiler == 'ein' :        # NT-Ladung Boiler einschalten
                NT_Ladung_Boiler = True         # aber
                if KTakt >= KTmax :             # nur , wenn max. Temperatur n.n. erreicht
                    NT_Ladung_Boiler = False    
                    print ("-- Boiler NT-Ladung nicht aktiv max.Temperatur erreicht",BTakt)
                else :
                    print ("-- Boiler NT-Ladung aktiv von",BNvon,"bis",BNbis,'aktuell',BTakt)
            else :
                NT_Ladung_Boiler = False        # wenn nein , keine Nachtladung
                print     ("-- Boiler NT-Ladung nicht aktiv , nur von",BNvon,"bis",BNbis,'aktuell',DTakt,)
                # Prüfung , ob alternativ Direktladung einzuschalten ist
                Histgrenze = BTmin                  # Prüfung , ob Histerese läuft
                if BTakt > BTmin and BTakt < (BTmin + BThist) :  
                    Histgrenze = BTmin + BThist     # Histerese läuft bis Grenze
                if BTakt < Histgrenze :             # Direktladung einschalten
                    Direktladung_Boiler = True     
                    TextString = "-- Direktladung     aktiv aktuell " + str(BTakt) + " unter Minimum " + str(BTmin)
                    TextString = TextString + ' Histerese bis ' + str(BTmin + BThist)
                    print (Fore.YELLOW + TextString)
                else :
                    Direktladung_Boiler = False
                    print     ("-- Boiler Direktladung nicht aktiv")   

        else :
            print ('Warmwasserbereitung Steuerung ausgeschaltet')
            # Relais für den Boiler :  wird bzw. bleibt ausgeschaltet !
            NT_Ladung_Boiler      = False
            Direktladung_Boiler   = False
        
        # Abbruch , wenn weder Raumheizung noch Warmwasser eingeschaltet
        if not (Raumheizung or Warmwasser or Sonstige) :
            TextString = 'weitere Verarbeitung nicht sinnvoll , weder Raumheizung noch Warmwasser eingeschaltet'
            TextString = TextString + '\n'   # neue Zeile
            TextString = TextString + 20 * ' ' + 'Parameter korrigieren in : /home/pi/skripts/prod/Parameter.json'
            raise AssertionError (TextString)
                
        # Beginn Relais - Schaltvorgänge ###########################################################################
        #  Aktionen Kessel und Tagsteuerung nur , wenn Raumheizung eingeschaltet ist !
        TextString = Style.BRIGHT + 'Schaltvorgänge  :   '+ Style.RESET_ALL  
        TextString = TextString + "(Hintergrund rot->aus,grün->ein  Schrift weiß->unverändert,schwarz->geschaltet)"
        print (TextString) 
        
        if Raumheizung : 
            
            TextString = Style.BRIGHT +'- Raumheizung   :'
            print (TextString)
            
            # Setzen Parameter zur Schaltung von Relais WK1 für die Funktion Tag-/Nachtbetrieb
            RELAIS       = 'WK1'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            loggen       = True             # True = ja , False = nein
            # für Tagbetrieb Tagsteuerung=True=einschalten , für Nachtbetrieb Tagsteuerung=False=ausschalten
            # Schaltvorgang durchführen
            print (Func_Relais.Schaltung (RELAIS , Tagsteuerung , drucken , loggen))
            time.sleep(1)
            
            # Setzen Parameter zur Schaltung von Relais WK2 für die Funktion boost
            RELAIS       = 'WK2'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            loggen       = True             # True = ja , False = nein    
            # boost=True=einschalten , boost=False= ausschalten
            # Schaltvorgang durchführen
            print (Func_Relais.Schaltung (RELAIS , boost , drucken , loggen))
            time.sleep(1)
                        
            # Schaltung Relais K2 für die Heizung  im Keller
            # Parameter bereits gesetzt bei Entscheid Nacht- oder Direktladung , Kessel oder Boiler
            RELAIS       = K2_Relais        # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            loggen       = True             # True = ja , False = nein    
            # welches Relais (K2_Relais) wie (K2_Schalter) geschaltet wird ist weiter oben entschieden 
            # Schaltvorgang durchführen
            print (Func_Relais.Schaltung (RELAIS , K2_Schalter , drucken , loggen))
            time.sleep(1)
            
        #  keine Raumheizung --> alle Relais ausschalten , die davon betroffen sind !           
        else :
            TextString = Fore.YELLOW + 'Raumheizung         und zugehörige Relais WK1,WK2,KK2<HK2,DK2> ausgeschaltet' 
            print (TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            loggen           = True
            RELAIS = 'WK1'
            TextString = (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten
            RELAIS = 'WK2'
            TextString = (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten
            RELAIS = 'KK2'  # KK2 = HK2 = DK2 , gleiches Relais
            TextString = (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten

        #  Aktionen Boiler nur , wenn Warmwasser eingeschaltet ist !
        if Warmwasser :
            TextString = Style.BRIGHT +'- Warmwasser    :'
            print (TextString)      
            if NT_Zeit_Boiler == 'ein'  :       # Schaltung Nachtaufladung
                # Setzen Parameter zur Schaltung von Relais BK1 für die Funktion Nachtaufladung Boiler
                RELAIS = 'BK1'  # NT_Ladung_Boiler
                drucken      = True             # True = ja , False = nein
                loggen       = True             # True = ja , False = nein    
                # NT_Ladung_Boiler=True=einschalten , NT_Ladung_Boiler=False= ausschalten
                # Schaltvorgang durchführen
                print (Func_Relais.Schaltung (RELAIS , NT_Ladung_Boiler , drucken , loggen))
                time.sleep(1)
                                        
            else  :                             # Schaltung Direktaufladung
                # Setzen Parameter zur Schaltung von Relais DK1 für die Funktion Direktladung Boiler noch nicht implementiert
                RELAIS = 'DK1'  # Direktladung_Boiler
                drucken      = True             # True = ja , False = nein
                loggen       = True             # True = ja , False = nein    
                # Direktladung_Boiler=True=einschalten , Direktladung_Boiler=False= ausschalten
                # Schaltvorgang durchführen
                print (Func_Relais.Schaltung (RELAIS , Direktladung_Boiler , drucken , loggen))
                time.sleep(1)
                     
        #  Keine Warmwasserbereitung -->  Relais Boiler ausschalten          
        else :  
            TextString = Fore.YELLOW + 'Warmwasserbereitung und zugehörige Relais KK1<BK1,DK1> ausgeschaltet' + Style.RESET_ALL 
            print (TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            loggen           = True
            RELAIS = 'KK1'   # KK1 = BK1 = DK1 , gleiches Relais
            TextString = (Func_Relais.Schaltung (RELAIS , Schalter  , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten

        # Sonstige Schaltvorgänge
        if Sonstige :
            TextString = Style.BRIGHT + '- Sonstige      :'
            print (TextString)
            
            # Setzen Parameter zum Pingen von Relais WK3 für TFA 3035 pingen
            RELAIS       = 'WK3'            # Relais wie in Relais-Tabelle definiert
            drucken      = False            # True = ja , False = nein
            loggen       = False            # True = ja , False = nein    
            Schalter     = True             # Ping ein
            # Schaltvorgang durchführen
            #print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))
            Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen)
            time.sleep(1)                   # 1 sec warten
            Schalter     = False            # Ping aus
            # Schaltvorgang durchführen
            Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen)
            TextString = Fore.CYAN +' Relais '+ RELAIS + ' TFA 3035 angepingt ohne weitere Aktion ' 
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
            print (TextString)
            time.sleep(1)
            
            # Setzen Parameter zum Schalten von Relais GK1 Garten
            RELAIS       = 'GK1'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            loggen       = True             # True = ja , False = nein
            TextString   = Fore.RESET + 20*' '
            if SoLo_Bezug >= PVmin :        # nur einschalten , wenn ausreichender PV-Ertrag
                Schalter     = True
                TextString      = TextString + '(Einspeisung für Garten ausreichend ' + str(SoLo_Bezug) + ' >= PVmin ' + str(PVmin) + ')'
            else :
                Schalter     = False
                if SoLo_Bezug >= 0 :
                    TextString  = TextString + '(Einspeisung für Garten nicht ausreichend ' + str(SoLo_Bezug) + ' < PVmin ' + str(PVmin) + ')'
                else :
                    TextString  = TextString + '(Einspeisung für Garten nicht ausreichend , da Bezug negativ ' + str(SoLo_Bezug) + ')'
            # Schaltvorgang durchführen
            #print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))
            print (Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen))
            print (TextString)
            time.sleep(1)                   # 1 sec warten
        
        #  keine Sonstige --> alle Relais ausschalten , die davon betroffen sind !   
        else :
            TextString = Fore.YELLOW + 'Sonstige            und zugehörige Relais WK3,GK1 ausgeschaltet' + Style.RESET_ALL 
            print (TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            loggen           = True
            RELAIS = 'WK3'   # ping-Relais
            TextString = (Func_Relais.Schaltung (RELAIS , Schalter  , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten
            RELAIS = 'GK1'   # Garten-Relais
            TextString = (Func_Relais.Schaltung (RELAIS , Schalter  , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten
            
        # Ende Schaltvorgänge #######################################################################################
        if iverarb == 1   : wait = wait / 2 # beim 1. Lauf nur 1/2 Zeit warten
        TextString = ' ENDE Entladesteuerung     ' + str(iverarb + 1) + '. Lauf beginnt in ' + str(wait) + ' Sekunden ----------------'
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
        print (Fore.GREEN + TextString)
        
        # Ende Endlosschleife nächster Lauf zyklisch nach x Sekunden
        time.sleep(wait)        
        
        
except KeyboardInterrupt as e :
    # Programm beendet mit CTRL+C
    print ()
    END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") + ' ENDE Entladesteuerung mit KeyboardInterrupt (CTRL+C oder Strg+C)'
    print (Fore.GREEN + END_TEXT)
    END_TEXT = 20 * ' ' + str(e)
    print (Fore.GREEN + END_TEXT)
    END_TEXT = ''
    
except AssertionError as e :
    # Programm beendet mit AssertionError
    END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") + ' ENDE Entladesteuerung mit AssertionError :'
    print (Fore.RED + Style.BRIGHT + END_TEXT)
    END_TEXT = 20 * ' ' + str(e)
    print (Fore.RED + Style.BRIGHT + END_TEXT)
        
except Exception as e :
    print ()
    END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") + ' ENDE Entladesteuerung mit Exception :'
    print (Fore.RED + Style.BRIGHT + END_TEXT)
    END_TEXT = 20 * ' ' + str(e)
    print (Fore.RED + Style.BRIGHT + END_TEXT)
#    sys.exit(1)

finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    if END_TEXT == '' :
        END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") + ' ---> Entladesteuerung fehlerfrei beendet' 
        print (Fore.GREEN + Style.BRIGHT + END_TEXT )
    print ()
    sys.exit(0)

