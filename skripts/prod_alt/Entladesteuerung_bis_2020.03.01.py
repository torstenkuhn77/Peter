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
init()

# eigene Routinen
import Func_Temp_Sens      # Funktion zum Abfragen der Temperatursensoren
import Func_Relais         # Funktion zum Schalten der Relais
import Func_Solar_Log      # Funktion zum Lesen aus Solar-Log JSON
import Func_NT_Ladung      # Funktion zur Prüfung , ob Nachttarifladung eines Gerätes möglich 
import GVS                 # Zwischenspeicher eigene globale Variablen

END_TEXT = ''

try:
    
    # Anzahl Verarbeitungsvorgänge
    iverarb  = 0
    
    # Endlosschleife
    while True :                                  
        
        # JSON Datei mit Parametern einlesen
        with open('/home/pi/skripts/prod/Parameter.json') as f:
            config_raw = f.read()
        # Konvertieren der gelesenen bytes in einen JSON string
        config = json.loads(config_raw)
        
        # Parameter setzen , prüfen , Istwerte ermitteln
        
        if config['Parameter']['Raumheizung'] == 'ein' : Raumheizung = True
        else : Raumheizung = False
        if config['Parameter']['Warmwasser']  == 'ein' : Warmwasser  = True
        else : Warmwasser = False
        if not (Raumheizung or Warmwasser) :
            raise AssertionError (' Verarbeitung nicht möglich , weder Raumheizung noch Warmwasser eingeschaltet')

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
        
                
        # Beginn Verarbeitung
        iverarb = iverarb + 1
        
        print ()
        TextString = ' START Entladesteuerung    ' + str(iverarb) + '. Lauf -----------------------------------------'
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
        print (Fore.GREEN + TextString)
                
        if iverarb == 1 :
            print ("Steuerungsparameter,aktuelle Werte : (Zeiten hh:mm , Temperaturen Grad Celsius)")        
            print ('                   ','Heizung ' ,config['Parameter']['Raumheizung'],' Warmwasser ',config['Parameter']['Warmwasser']) 
        
        # Ausgabe Istwerte
        print ("Raumtemperatur      aktuell",RTakt,"max",RTmax,'min',RTmin)
        print ("Boilertemperatur    aktuell",BTakt,"max",BTmax,"min",BTmin,'hist ',BThist,'(NT-Ladung von',BNvon,'bis',BNbis,')')
        if BTakt < BTmin :
            print (Fore.YELLOW +
               '                    Minimum unterschritten -->  Direktladung erforderlich !')
        print ("Kesseltemperatur    aktuell",KTakt,"max",KTmax,"min",KTmin,'hist',KThist,'(NT-Ladung von',KNvon,'bis',KNbis,')')
        if KTakt < KTmin :
            print (Fore.YELLOW +
               '                    Minimum unterschritten -->  Direktladung erforderlich !')
        print ("Vorlauftemperatur   aktuell",VTakt,"max",VTmax)
                
        #localIP = '169.254.34.32'                                   # lokale IP des Solar-Log aus GVS
        SoLo_Text = Func_Solar_Log.Lesen(GVS.SolarLog_localIP)       # Solar-log JSON lesen
                                                                     # Solar-log Bezug lesen
        SoLo_Bezug = (round((GVS.SolarLog_Erzeugung - GVS.SolarLog_Verbrauch),2))
        
        # Entscheid , ob Tagsteuerung , ggf. Nachtabsenkung
        if RTakt < RTmin :
            Tagsteuerung = True
            print    ("Tagbetrieb          immer aktiv , wenn Raumtemperatur",RTakt,'unter',RTmin)
        else :
            if DTakt >= DTvon and DTakt <= DTbis :
                Tagsteuerung = True
            else :
                Tagsteuerung = False
                print ("kein Tagbetrieb     Nachtabsenkung von",DTbis,"bis",DTvon,'aktuell',DTakt)
            if  Tagsteuerung and GVS.SolarLog_Erzeugung < PVmin :
                Tagsteuerung = False
                print ("Tagbetrieb         ",DTvon,"bis",DTbis,Fore.YELLOW +
                       ' aber Nachtabsenkung ','PV-Erzeugung nicht ausreichend (min',PVmin,')')
            if  Tagsteuerung and VTakt > VTmax :
                Tagsteuerung = False
                print ("Tagbetrieb         ",DTvon,"bis",DTbis,Fore.YELLOW +
                       ' aber Nachtabsenkung ','Vorlauftemperatur',VTakt,'über Maximum',VTmax)
            if  Tagsteuerung and KTakt < KTmin + KThist :
                Tagsteuerung = False
                print ("Tagbetrieb         ",DTvon,"bis",DTbis,Fore.YELLOW  +
                       ' aber Nachtabsenkung ','Kesseltemperatur',KTakt,'unter',KTmin + KThist,'(min + hist)')
            if  Tagsteuerung :
                print ("Tagbetrieb          aktiv von",DTvon,"bis",DTbis,'aktuell',DTakt)
        
        # Entscheid , ob boost eingeschaltet wird
        if Tagsteuerung :
            boost = True
        else :
            boost = False
            print ('boost               nicht aktiv bei Nachtabsenkung')
        if SoLo_Bezug < 0  and boost :
            boost = False
            print ('boost               nicht aktiv , kein PV-Überschuss (Bezug ' , SoLo_Bezug, ')')
        if KTakt < KTboost and boost :
            boost = False
            print ('boost               nicht aktiv Kesseltemperatur unter ',KTboost)
        if VTakt > VTmax   and boost :
            boost = False
            print ('boost               nicht aktiv Vorlauftemperatur größer ',VTmax)
        if RTakt > RTmax   and boost :
            boost = False
            print ('boost               nicht aktiv Raumtemperatur größer ',RTmax)
        if DTakt < BZvon   and boost :
            boost = False
            print ('boost               nicht aktiv erst ab ',BZvon,' verfügbar')
        if DTakt > BZbis   and boost :
            boost = False
            print ('boost               nicht aktiv nur bis ',BZbis,' verfügbar')
        if boost :
            print ("boost               aktiv von ",BZvon,' bis ',BZbis,' bei ',KTboost,' Einspeisung ',SoLo_Bezug)
        else :
            if RTakt < RTmin :
                boost = True
                print (Fore.RED +
                   "boost               aktiv weil Raumtemperatur " + str(RTakt) + " unter Minimum " + str(RTmin) + '!')
                
        print     ("Nachttarif          von " ,NT_Zeit_Start,' bis ',NT_Zeit_Ende,' NT-Tarif mit Preisreduktion')
        
        # Entscheid , ob fǘr Nachtaufladung Boiler eingeschaltet wird
        # Prüfung Plausibilität der Ladezeiten
        if Func_NT_Ladung.pruef (NT_Zeit_Start,NT_Zeit_Ende,BNvon,BNbis,DTvon,DTbis,DTakt) :
            print     (Fore.RED + "Boiler NT-Ladung    nicht aktiv , falsche Parameter , keine Nachtladung möglich !")
            print     (           "                    Ladezeit",BNvon,'bis',BNbis,'außerhalb NT-Intervall',NT_Zeit_Start,'bis',NT_Zeit_Ende)
            print     (           "                    oder Überschneidung  NT-Intervall / Tagzeit")
            raise ValueError (Fore.RED + " daher weitere Verarbeitung nicht möglich")
        
        NT_Ladung_Boiler = GVS.NT_Ladung_Geraet  
        
        if NT_Ladung_Boiler :               # wenn ja , Nachtladung
            if BTakt >= BTmax :
                NT_Ladung_Boiler = False    # nur , wenn max. Temperatur n.n. eereicht
                print ("Boiler NT-Ladung    nicht aktiv max.Temperatur erreicht",BTakt)
            else :
                print ("Boiler NT-Ladung    aktiv von",BNvon,"bis",BNbis,'aktuell',DTakt)
        else :                              # wenn nein , keine Nachtladung
            print     ("Boiler NT-Ladung    nicht aktiv , nur von",BNvon,"bis",BNbis,'aktuell',DTakt,)
            
        # Entscheid , ob fǘr Nachtaufladung Kessel eingeschaltet wird
        # Prüfung Plausibilität der Ladezeiten
        if Func_NT_Ladung.pruef (NT_Zeit_Start,NT_Zeit_Ende,KNvon,KNbis,DTvon,DTbis,DTakt) :
            print     (Fore.RED + "Boiler NT-Ladung    nicht aktiv , falsche Parameter , keine Nachtladung möglich !")
            print     (           "                    Ladezeit",KNvon,'bis',KNbis,'außerhalb NT-Intervall',NT_Zeit_Start,'bis',NT_Zeit_Ende)
            print     (           "                    oder Überschneidung  NT-Intervall / Tagzeit")
            raise ValueError (Fore.RED + " daher weitere Verarbeitung nicht möglich")
        
        NT_Ladung_Kessel = GVS.NT_Ladung_Geraet  
        
        if NT_Ladung_Kessel :               # wenn ja , Nachtladung
            if BTakt >= BTmax :
                NT_Ladung_Kessel = False    # nur , wenn max. Temperatur n.n. eereicht
                print ("Kessel NT-Ladung    nicht aktiv max.Temperatur erreicht",BTakt)
            else :
                print ("Kessel NT-Ladung    aktiv von",KNvon,"bis",KNbis,'aktuell',DTakt)
        else :                              # wenn nein , keine Nachtladung
            print     ("Kessel NT-Ladung    nicht aktiv , nur von",KNvon,"bis",KNbis,'aktuell',DTakt,)
            
        # Prüfung , ob Direktladung Boiler einzuschalten ist
        if BTakt < BTmin :
            Direktladung_Boiler = True
        else :
            Direktladung_Boiler = False
        
        # Prüfung , ob Direktladung Kessel einzuschalten ist
        if KTakt < KTmin :
            Direktladung_Kessel = True
        else :
            Direktladung_Kessel = False
        
        print (SoLo_Text,'PVmin =',PVmin)   # Text des Solar-Log Drucken mit Angabe PVmin       
        
        # Beginn Relais - Schaltvorgänge
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + Fore.GREEN + " Schaltvorgänge : "
        TextString = TextString + Fore.RESET + "(rot-> aus , grün-> ein , weiß-> unverändert , schwarz-> geschaltet)"
        print (TextString)
        
        # Setzen Parameter zur Schaltung von Relais WK1 für die Funktion Tag-/Nachtbetrieb
        RELAIS       = 'WK1'            # Relais wie in Relais-Tabelle definiert
        drucken      = True             # True = ja , False = nein
        loggen       = True             # True = ja , False = nein
        # für Tagbetrieb Tagsteuerung=True=einschalten , für Nachtbetrieb Tagsteuerung=False=ausschalten
        # Schaltvorgang durchführen
        print (Func_Relais.Schaltung (RELAIS , Tagsteuerung , drucken , loggen))

        # Setzen Parameter zur Schaltung von Relais WK2 für die Funktion boost
        RELAIS       = 'WK2'            # Relais wie in Relais-Tabelle definiert
        drucken      = True             # True = ja , False = nein
        loggen       = True             # True = ja , False = nein    
        # boost=True=einschalten , boost=False= ausschalten
        # Schaltvorgang durchführen
        print (Func_Relais.Schaltung (RELAIS , boost , drucken , loggen))
        
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
        print ()
        
        
        # Setzen Parameter zum Test des unbenutzten Relais WK4 nur beim 1. Schaltvorgang
        if iverarb == 1 :
            RELAIS       = 'WK4'            # Relais wie in Relais-Tabelle definiert
            drucken      = False            # True = ja , False = nein
            loggen       = False            # True = ja , False = nein    
            Schalter     = True             # Ping ein
            # Schaltvorgang durchführen
            Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen)
            time.sleep(1)                   # 1 sec warten
            Schalter     = False            # Ping aus
            # Schaltvorgang durchführen
            Func_Relais.Schaltung (RELAIS , Schalter , drucken , loggen)
            TextString = Fore.CYAN +' Relais '+ RELAIS + ' zum Test angepingt ohne weitere Aktion nur beim 1. Lauf' 
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
            print (TextString)
            print ()
            
        
        # Setzen Parameter zum Test der Funktion Nachtaufladung Boiler noch nicht implementiert
        if NT_Ladung_Boiler :
            RELAIS = 'NT- Ladung Boiler'
            TextString = Fore.BLUE +' Relais '+ RELAIS + ' Funktion noch nicht Implementiert' 
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
            print (TextString)
            print ()

        # Setzen Parameter zum Test der Funktion Nachtaufladung Kessel noch nicht implementiert
        if NT_Ladung_Kessel :
            RELAIS = 'NT- Ladung Kessel'
            TextString = Fore.BLUE +' Relais '+ RELAIS + ' Funktion noch nicht Implementiert' 
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
            print (TextString)
            print ()

        # Setzen Parameter zum Test der Funktion Direktladung Boiler noch nicht implementiert
        if Direktladung_Boiler :
            RELAIS = 'Direktladung Boiler'
            TextString = Fore.BLUE +' Relais '+ RELAIS + ' Funktion noch nicht Implementiert' 
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
            print (TextString)
            print ()

        # Setzen Parameter zum Test der Funktion Direktladung Kessel noch nicht implementiert        
        if Direktladung_Kessel :
            RELAIS = 'Direktladung Kessel'
            TextString = Fore.BLUE +' Relais '+ RELAIS + ' Funktion noch nicht Implementiert' 
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
            print (TextString)
            print ()


        # Ende Schaltvorgänge
        if iverarb == 1   : wait = 20 # beim 1. Lauf 20 sec warten
        TextString = ' ENDE Entladesteuerung     ' + str(iverarb + 1) + '. Lauf beginnt in ' + str(wait) + ' Sekunden ----------------'
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
        print (Fore.GREEN + TextString)
        # Ende Endlosschleife nächster Lauf zyklisch nach x Sekunden
        #print ()
        time.sleep(wait)        
        
        
except KeyboardInterrupt :
    # Programm beendet mit CTRL+C
    print ()
    END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") +    ' ENDE Entladesteuerung mit KeyboardInterrupt (CTRL+C / Strg+C)' 
    print (Fore.GREEN + END_TEXT)
    END_TEXT = ''
    
except AssertionError as e:
    # Programm beendet mit AssertionError
    print ()
    END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") + str(e)
    print (Fore.RED + Style.BRIGHT + END_TEXT)
    END_TEXT = '                    in : /home/pi/skripts/prod/Parameter.json'
    print (Fore.RED + Style.BRIGHT + END_TEXT)
        
except Exception as e:
    print ()
    END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") +    ' ENDE Entladesteuerung mit Exception ' + str(e)
    print (Fore.RED + Style.BRIGHT + END_TEXT)
    sys.exit(1)

finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    if END_TEXT == '' :
        END_TEXT = time.strftime("%Y.%m.%d %H:%M:%S") + ' -->  Entladesteuerung fehlerfrei beendet' 
        print (Fore.GREEN  + END_TEXT )
    print ()
    sys.exit(0)

