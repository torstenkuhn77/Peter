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
import Temp_Sens_Abfrage   # Funktion zum Abfragen der Temperatursensoren
import Func_Relais         # Funktion zum Schalten der Relais
import Func_Solar_Log      # Funktion zum Lesen aus Solar-Log JSON
import Func_NT_Ladung      # Funktion zur Prüfung , ob Nachttarifladung eines Gerätes möglich 
import GVS                 # Zwischenspeicher eigene globale Variablen

try:
    
    # Anzahl Verarbeitungsvorgänge
    iverarb = 0                                    
    
    # Endlosschleife
    while True :                                  
              
        # JSON Datei mit Parametern einlesen
        with open('/home/pi/skripts/prod/Parameter.json') as f:
            config_raw = f.read()
        # Konvertieren der gelesenen bytes in einen JSON string
        config = json.loads(config_raw)
        
        # Parameter setzen , Istwerte ermitteln
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
        sensorRT = Temp_Sens_Abfrage.sensorRT
        RTakt = Temp_Sens_Abfrage.readTempLines(sensorRT)[0]
        RTmin = config['Parameter']['Raumtemperatur']['RTmin']
        RTmax = config['Parameter']['Raumtemperatur']['RTmax']
        # Boilertemperatur  aktuell , min , max , hist , Nachtladung
        # Sensor 28-0316a27937aa
        sensorBT = Temp_Sens_Abfrage.sensorBT
        BTakt  =   Temp_Sens_Abfrage.readTempLines(sensorBT)[0]
        BTmin  = config['Parameter']['Boilertemperatur']['BTmin']
        BTmax  = config['Parameter']['Boilertemperatur']['BTmax']
        BThist = config['Parameter']['Boilertemperatur']['BThist']
        BNvon  = config['Parameter']['NT_Aufl_Boiler']['BNvon']
        BNbis  = config['Parameter']['NT_Aufl_Boiler']['BNbis']
        # Vorlauftemperatur , aktuell , max
        # Sensor 28-030997790e32
        sensorVT = Temp_Sens_Abfrage.sensorVT
        VTakt = Temp_Sens_Abfrage.readTempLines(sensorVT)[0]
        VTmax = config['Parameter']['Vorlauftemperatur']['VTmax']
        # Kesseltemperatur aktuell , min , max , boosttemperatur , boostzeit , Nachtladung
        # Sensor 28-030997790a01
        sensorKT = Temp_Sens_Abfrage.sensorKT
        KTakt   = Temp_Sens_Abfrage.readTempLines(sensorKT)[0]
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
        
        # Ausgabe Istwerte
        print ("Raumtemperatur      aktuell",RTakt,"max",RTmax,'min',RTmin)
        print ("Boilertemperatur    aktuell",BTakt,"max",BTmax,"min",BTmin,'hist ',BThist,'(NT-Ladung von',BNvon,'bis',BNbis,')')
        print ("Kesseltemperatur    aktuell",KTakt,"max",KTmax,"min",KTmin,'hist',KThist,'(NT-Ladung von',KNvon,'bis',KNbis,')')
        print ("Vorlauftemperatur   aktuell",VTakt,"max",VTmax)
                
        localIP = '169.254.34.32'                                    # lokale IP des Solar-Log
        SoLo_Text = Func_Solar_Log.Lesen(localIP)                    # Solar-log JSON lesen
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
                print ("Nachtabsenkung      aktiv von",DTbis,"bis",DTvon,'aktuell',DTakt)
            if  Tagsteuerung and GVS.SolarLog_Erzeugung <= 1 :
                Tagsteuerung = False
                print ("Tagbetrieb          von",DTvon,"bis",DTbis)
                print ('                    aber Nachtabsenkung PV-Erzeugung nicht ausreichend (min',PVmin,')')
            if  Tagsteuerung and VTakt > VTmax :
                Tagsteuerung = False
                print ("Tagbetrieb          von",DTvon,"bis",DTbis)
                print ('                    aber Nachtabsenkung Vorlauftemperatur',VTakt,'über Maximum',VTmax)
            if  Tagsteuerung and KTakt < KTmin + KThist :
                Tagsteuerung = False
                print ("Tagbetrieb          von",DTvon,"bis",DTbis)
                print ('                    aber Nachtabsenkung Kesseltemperatur',KTakt,'unter',KTmin + KThist,'(min + hist)')
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
            print ('boost               nicht aktiv Kesseltemperatur unter',KTboost,')')
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
        
        print     ("Nachttarif          von" ,NT_Zeit_Start,'bis',NT_Zeit_Ende,' NT-Tarif mit Preisreduktion')
        
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
        
        
        print (SoLo_Text,'PVmin =',PVmin)                             # Text des Solar-Log Drucken
                                                                      # + Angabe PVmin       
        print ()                                                      # Leerzeile
        
        # Beginn Schaltvorgänge

        print (time.strftime("%Y.%m.%d %H:%M:%S") + Fore.GREEN + " Schaltvorgänge :")
        
        
        # Setzen Parameter zur Schaltung von Relais für die Funktion Tag-/Nachtbetrieb
        Funktion     = ' Tagbetrieb                         '
        RELAIS       = 'WK1'
        RELAIS_GPIO  =  12
        # Schaltvorgang durchführen
        if Tagsteuerung :            
            Schalter     = 'ein'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        else :
            Schalter     = 'aus'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))

        # Setzen Parameter zur Schaltung von Relais für die Funktion boost
        Funktion     = ' boost                              '
        RELAIS       = 'WK2'
        RELAIS_GPIO  =  16
        # Schaltvorgang durchführen
        if boost :            
            Schalter     = 'ein'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        else :
            Schalter     = 'aus'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))

        # Setzen Parameter zum ping von Relais für die Funktion TFA 3035 pingen
        Funktion     = ' ping Funktemperaturstation TFA 3035'
        RELAIS       = 'WK3'
        RELAIS_GPIO  =  20
        Schalter     = 'ein'      # zulässig : ein , aus
        # Schaltvorgang durchführen
        print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        time.sleep(1)
        Schalter     = 'aus'      # zulässig : ein , aus
        print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        
        # Setzen Parameter zum Test des unbenutzten Relais nur beim 1. Schaltvorgang
        if iverarb == 1 :
            Funktion     = 'ping Test unbenutztes Relais       '
            RELAIS       = 'WK4'
            RELAIS_GPIO  =  21
            Schalter     = 'ein'      # zulässig : ein , aus
            # Schaltvorgang durchführen
            Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter)
            time.sleep(1)
            Schalter     = 'aus'      # zulässig : ein , aus
            Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter)
            print (time.strftime("%Y.%m.%d %H:%M:%S") ,Funktion,'Relais ' + RELAIS + ' GPIO ' + str(RELAIS_GPIO) + ' erledigt')
        
        # Setzen Parameter zum Test der Funktion Nachtaufladung Boiler noch nicht aktiv
        Funktion     = ' Test Boiler NT-Ladung              '
        RELAIS       = 'WK4'
        RELAIS_GPIO  =  21
        # Schaltvorgang durchführen
        if NT_Ladung_Boiler :            
            Schalter     = 'ein'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        else :
            Schalter     = 'aus'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        
        # Setzen Parameter zum Test der Funktion Nachtaufladung Kessel noch nicht aktiv
        Funktion     = ' Test Kessel NT-Ladung              '
        RELAIS       = 'WK4'
        RELAIS_GPIO  =  21
        # Schaltvorgang durchführen
        if NT_Ladung_Kessel :            
            Schalter     = 'ein'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        else :
            Schalter     = 'aus'   # zulässig : ein , aus
            print (Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter))
        
        
        # Ende Schaltvorgänge

        TextString = ' ENDE Entladesteuerung     ' + str(iverarb + 1) + '. Lauf beginnt in ' + str(wait) + ' Sekunden ----------------'
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
        print (Fore.GREEN + TextString)

        # Ende Endlosschleife nächster Lauf zyklisch nach x Sekunden
        print ()
        time.sleep(wait)        
        
        
except KeyboardInterrupt:
    # Programm beendet mit CTRL+C
    print ()
    print      (Fore.YELLOW + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S")  +
                ' ENDE Entladesteuerung durch CTRL+C / Strg+C')
        
except Exception as e:
    print ()
    print      (Fore.RED + Back,WHITE + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + ' Exception')
    print      (Fore.RED + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + str(e))
    sys.exit(1)

finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    print ()
    print       (Fore.RED + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") +
                 ' Programm Entladesteuerung abgebrochen')
    sys.exit(0)

