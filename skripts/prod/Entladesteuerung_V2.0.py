# shell : python3 /home/pi/skripts/prod/Entladesteuerung_V1.7.py
#         @/usr/bin/python3 /home/pi/skripts/prod.Entladesteuerung_V1.7.py

# -*- coding: utf-8 -*-   

# System- und fremde Funktionen ###########################################################
import time,sys ,RPi.GPIO as GPIO ,json
import logging 
from Logger import Logger

# eigene externe Routinen #################################################################
import Func_Sens           # Funktion zum Auslesen eines Temperatursensors
import Func_Relais         # Funktion zum Set / Reset von Relais
import Func_Solar_Log      # Funktion zum Lesen aus Solar-Log JSON Schnittstelle
import Func_Geraet         # Funktion Ausgabe Gerätetemperatur , Prüfung Nachtaufladung und ob Histerese ein / aus / bleibt 
import GVS                 # Zwischenspeicher eigene globale Variablen
import Func_LogDatei       # Funktion Logdatei schreiben
# eigene externe Routinen Ende ############################################################

log = Logger() 
logScreen = log.GetLogger("Screen") # nur Console Ausgaben
logMain = log.GetLogger("Main")     # Console/File Ausgaben

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
    
    print()
    TextString = 'Neustart Entladesteuerung  ' + Version + '  Initialisierung :'
    logMain.log(logging.INFO, TextString)

    # Initialisierung / Reset aller Relais
    # Setzen Parameter zur Initialisierung aller Relais
    drucken      = True           # True = drucken , False = nein
    loggen       = 'RelTab'       # aus RelTab oder True = loggen , False = nein
    RELAIS       = 'alle'         # alle Relais wie in Relais-Tabelle GVS.RelTab() definiert
    # Initialisierung durchführen Schalten , ggf.Ergebnis drucken , loggen
    Schalter     = False         # True = ein , False = aus
    result = Func_Relais.Reset(RELAIS , Schalter , drucken , loggen)
    logScreen.log(logging.INFO, result)

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
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
        logScreen.log(logging.INFO, TextString)
        
        if iverarb == 1 :  # Informationen zu Steuerungsparametern , Nachttarif etc. nur beim 1. Lauf
            print (19 * ' ',"Steuerungsparameter,aktuelle Werte : (Zeiten hh:mm Temperaturen Grad Celsius)")    
        
        # aus Systembus die Werte aller Sensoren vom Typ DS18B20 auslesen , in GVS.SensTab speichern und ausdrucken
        Typ = 'DS18B20'      # Sensor Typ
        i_les_Sens     = 0   # Zähler Leseversuche ONE-Wire Bus
        i_les_Sens_max = 3   # max Anzahl Leseversuche ONE-Wire Bus
        les_wait       = 10  # Sekunden Wartezeit bei Unterbrechung ONE-Wire Bus
        Ergebnis = 'Fehler'  # Annahme : shit happens
        
        while 'Fehler' in Ergebnis and i_les_Sens < i_les_Sens_max :
            i_les_Sens = i_les_Sens + 1
            Ergebnis = str(Func_Sens.les_alle (Typ))
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + ' Ergebnis Auslesen aller Sensoren '
            TextString = TextString + Typ + ' ' + str(i_les_Sens) + '. Versuch '
            if 'Fehler' in Ergebnis :              # Fehler --> Nachlesen
                if i_les_Sens == i_les_Sens_max :  # Nachlesen erfolglos max Anzahl Leseversuche erreicht
                    TextString = time.strftime("%Y.%m.%d %H:%M:%S") + ' Auslesen aller Sensoren '
                    TextString = TextString + Typ + ' auch ' + str(i_les_Sens) + '. und letzter Versuch '
                    TextString = Fore.RED    + TextString + ' erfolglos '
                    print (TextString)
                    raise AssertionError (Ergebnis)
                else :                             # x Mal Nachlesen , ONE-Wire Bus reset
                    TextString = time.strftime("%Y.%m.%d %H:%M:%S") + ' Warnung : Auslesen aller Sensoren '
                    TextString = TextString + Typ + ' ' + str(i_les_Sens) + '. Versuch '
                    TextString = Fore.YELLOW + TextString + ' fehlerhaft --> Wiederholung nach ONE-Wire reset'
                    print (TextString)
                    # ONE-Wire Bus unterbrechen und neuer Versuch ##############################
                    # Setzen Parameter zur Unterbrechung des ONE-Wire Bus
                    drucken    = True           # True = ja , False = nein
                    loggen     = 'RelTab'       # aus RelTab oder True = ja , False = nein
                    RELAIS     = 'WK4'          # Relais wie in Relais-Tabelle GVS.RelTab() definiert
                    # Schaltvorgang zur Unterbrechung ONE-Wire Bus Schalten , Ergebnis drucken , loggen
                    Schalter   = True           # True = GND Ausschalten
                    U_Ergebnis = str((Func_Relais.Set (RELAIS , Schalter , drucken , loggen)))
                    if 'Fehler' in U_Ergebnis : # Fehler beim Ausschalten
                        print (Fore.RED   + 20 * ' ' + 'Abbruch : Fehler beim Ausschalten ONE-Wire Bus ')
                        raise AssertionError (U_Ergebnis)
                    else :
                        print (U_Ergebnis)
                    time.sleep (les_wait)       # Warten vor wieder Einschalten !
                    Schalter   = False          # False = GND wieder Einschalten
                    U_Ergebnis = str((Func_Relais.Set (RELAIS , Schalter , drucken , loggen)))
                    if 'Fehler' in U_Ergebnis : # Fehler beim Einschalten
                        print (Fore.RED   + 20 * ' ' + 'Abbruch : Fehler beim Einschalten ONE-Wire Bus ')
                        raise AssertionError (U_Ergebnis)
                    else :
                        print (U_Ergebnis)
                    time.sleep (les_wait)       # Warten vor dem nächsten Auslesen !
                    # Ende ONE-Wire Bus zurücksetzen und neuer Versuch #########################
                
            else :                              # Lesen erfolgreich
                print (TextString)
                print (Ergebnis)
                
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
            print (19 * ' ','(Zyklus Tag', wait ,'Nachtfaktor', NachtFaktor, 'Zyklus Nacht' , wait * NachtFaktor ,')')
        
        # Beginn Verarbeitung #########################################################################
        # Ausgabe Istwerte bei jedem Lauf unabhängig Raumheizung oder Warmwasserbereitung
        
        # Fotovoltaik-Informationen lesen und ausgeben          # lokale IP des Solar-Log aus GVS
        SoLo_Text = Func_Solar_Log.Lesen(GVS.SolarLog_localIP)  # Funktion Solar-log aus JSON-Datei lesen  
        if 'Fehler' in SoLo_Text :                              # Solar-log Fehler beim Lesen Warnung ausgeben
            SoLo_Text = time.strftime("%Y.%m.%d %H:%M:%S") + Fore.YELLOW + ' Warnung : ' + SoLo_Text
            SoLo_Bezug     = 0
            Solo_Erzeugung = 0                                  # Erzeugung und Bezug mit 0 angenommen
            print (SoLo_Text)
            print (Fore.YELLOW + 20 * ' ' + 'Erzeugung und Bezug für weitere Verarbeitung mit 0 angenommen !')
        else :                                                  # Solar-log Bezug und Erzeugung ermitteln
            SoLo_Bezug = (round((GVS.SolarLog_Erzeugung - GVS.SolarLog_Verbrauch), 2))
            Solo_Erzeugung = round(GVS.SolarLog_Erzeugung, 2)
            print (SoLo_Text,'Tagbetrieb erst ab PVmin',PVmin)
        
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
            TextString = Fore.YELLOW + TextString + ' , PV-Überschuß nicht ausreichend , Steuerung ausgeschaltet'
            print (TextString)
                
        # Ausgabe Istwerte nur relevant bei aktiver Raumheizung
        if Raumheizung :
            # Entscheid , ob Tagbetrieb oder Nachtabsenkung , entsprechende Ausgabe
            TextString = 'Raumheizung         eingeschaltet '
            # Tagbetrieb nur zwischen 7 und 21 Uhr zulässig !
            if DTvon >=  DTbis or DTvon < '07:00' or DTbis > '21:00' :
                TextString = 'weitere Verarbeitung nicht möglich , '
                if not DTbis > DTvon :
                    TextString = TextString + 'Tagbetrieb "bis" muß größer sein als "von"'
                else :
                    TextString = TextString + 'Tagbetrieb nur von 7 bis 21 Uhr'
                TextString = TextString + '\n'   # neue Zeile
                TextString = TextString + 20 * ' ' + 'Parameter korrigieren in : /home/pi/skripts/prod/Parameter.json'
                raise AssertionError (TextString)
            
            if SoLo_Bezug > PVmin :                      # ausreichender PV-Überschuß --> immer Tagsteuerung
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
            print (TextString)
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

            # Ausgabe Kesseltemperatur , Prüfung Nachtaufladung und ob Histerese ein / aus / bleibt #########################
            Ergebnis = Func_Geraet.pruef('Kessel', NT_Zeit_Start, NT_Zeit_Ende, KNvon, KNbis, DTvon, DTbis,
                                DTakt, KTakt, KTmin, KTmax, KThist)
            
            Rel_NameKessel    = Ergebnis.pop(0)   # 1. Parameter des Ergebnisses : betreffendes Relais
            Rel_SchKessel     = Ergebnis.pop(0)   # 2. Parameter des Ergebnisses : betreffender Schalter
            e                 = Ergebnis.pop(0)   # 3. Parameter des Ergebnisses : Fehlermeldung bei Abbruch

            if 'Fehler' in e :                    # Abbruch bei Programmfehler
                raise AssertionError (e)
            else :                                # Ausgabe Temperatur , Direkt- und Nachtladung
                print (e)

            # Ende Ausgabe Kesseltemperatur #################################################################################

            # Ausgabe Vorlauftemperatur
            if VTakt > VTmax :
                print ("- Vorlauftemperatur aktuell",VTakt,"max",VTmax,'überschritten')
            else :
                print ("- Vorlauftemperatur aktuell",VTakt,"max",VTmax)
            
            # Entscheid, ob boost eingeschaltet wird
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
            if not 'pausiert' in TextString :
                print ('Raumheizung         Steuerung ausgeschaltet')
            # Relais für Raumheizung und Kessel :  werden bzw. bleiben ausgeschaltet !
            Tagsteuerung          = False
            boost                 = False
        
        # Ausgabe Istwerte nur relevant für Warmwasserbereitung
        if Warmwasser :
            TextString = 'Warmwasserbereitung eingeschaltet '
            TextString = TextString + '(Nachttarif (NT) ' + NT_Zeit_Start + ' bis ' + NT_Zeit_Ende + ')'
            print (TextString)
            
            # Ausgabe Boilertemperatur , Prüfung Nachtaufladung und ob Histerese ein / aus / bleibt #########################

            Ergebnis = Func_Geraet.pruef('Boiler',NT_Zeit_Start,NT_Zeit_Ende,BNvon,BNbis,DTvon,DTbis,DTakt,BTakt,BTmin,BTmax,BThist)
            
            Rel_NameBoiler    = Ergebnis.pop(0)   # 1. Parameter des Ergebnisses : betreffendes Relais
            Rel_SchBoiler     = Ergebnis.pop(0)   # 2. Parameter des Ergebnisses : betreffender Schalter
            e                 = Ergebnis.pop(0)   # 3. Parameter des Ergebnisses : Fehlermeldung bei Abbruch

            if 'Fehler' in e :                    # Abbruch bei Programmfehler
                raise AssertionError (e)
            else :                                # Ausgabe Temperatur , Direkt- und Nachtladung
                print (e)

           # Ende Ausgabe Boilertemperatur #################################################################################
        
        else :
            print ('Warmwasserbereitung Steuerung ausgeschaltet')
        
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
            # für Tagbetrieb Tagsteuerung=True=einschalten , für Nachtbetrieb Tagsteuerung=False=ausschalten
            # Schaltvorgang durchführen
            print (Func_Relais.Set (RELAIS , Tagsteuerung , drucken , loggen))
            time.sleep(1)
            
            # Setzen Parameter zur Schaltung von Relais WK2 für die Funktion boost
            RELAIS       = 'WK2'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            # boost=True=einschalten , boost=False= ausschalten
            # Schaltvorgang durchführen
            print (Func_Relais.Set (RELAIS , boost , drucken , loggen))
            time.sleep(1)
                        
            # Schaltung Relais K2 für den Kessel im Keller
            # Parameter bereits gesetzt oben durch Funktion Func_Geraet.pruef
            RELAIS       = Rel_NameKessel   # Relais wie in Relais-Tabelle definiert
            Schalter     = Rel_SchKessel    # True = ein , False = aus
            drucken      = True             # True = ja , False = nein
            # Schaltvorgang durchführen            
            print (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))
            time.sleep(1)
            
        #  keine Raumheizung --> alle Relais ausschalten , die davon betroffen sind !           
        else :
            TextString = Fore.YELLOW + '- Raumheizung       und zugehörige Relais WK1,WK2,KK2<HK2,DK2> ausgeschaltet' 
            print (TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            RELAIS = 'WK1'
            TextString = (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten
            RELAIS = 'WK2'
            TextString = (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten
            RELAIS = 'KK2'  # KK2 = HK2 = DK2 , gleiches Relais
            TextString = (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten

        #  Aktionen Boiler nur , wenn Warmwasser eingeschaltet ist !
        if Warmwasser :
            TextString = Style.BRIGHT +'- Warmwasser    :'
            print (TextString)      
            # Schaltung Relais K1 für den Boiler im Keller
            # Parameter bereits gesetzt oben durch Funktion Func_Geraet.pruef
            RELAIS       = Rel_NameBoiler   # Relais wie in Relais-Tabelle definiert
            Schalter     = Rel_SchBoiler    # True = ein , False = aus
            drucken      = True             # True = ja , False = nein
            # Schaltvorgang durchführen
            print (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))
            time.sleep(1)

                     
        #  Keine Warmwasserbereitung -->  Relais Boiler ausschalten          
        else :  
            TextString = Fore.YELLOW + 'Warmwasserbereitung und zugehörige Relais KK1<BK1,DK1> ausgeschaltet' + Style.RESET_ALL 
            print (TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            RELAIS = 'KK1'   # KK1 = BK1 = DK1 , gleiches Relais
            TextString = (Func_Relais.Set (RELAIS , Schalter  , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten

        # Sonstige Schaltvorgänge
        if Sonstige :
            TextString = Style.BRIGHT + '- Sonstige      :'
            print (TextString)
            
            # Setzen Parameter zum Pingen von Relais WK3 für TFA 3035 pingen
            RELAIS       = 'WK3'            # Relais wie in Relais-Tabelle definiert
            drucken      = False            # True = ja , False = nein
            Schalter     = True             # Ping ein
            # Schaltvorgang durchführen
            Func_Relais.Set (RELAIS , Schalter , drucken , loggen)
            time.sleep(1)                   # 1 sec warten
            Schalter     = False            # Ping aus
            # Schaltvorgang durchführen
            Func_Relais.Set (RELAIS , Schalter , drucken , loggen)
            TextString = Fore.CYAN +' Relais '+ RELAIS + ' TFA 3035 angepingt ohne weitere Aktion ' 
            TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
            print (TextString)
            time.sleep(1)
            
            # Setzen Parameter zum Schalten von Relais GK1 Garten
            RELAIS       = 'GK1'            # Relais wie in Relais-Tabelle definiert
            drucken      = True             # True = ja , False = nein
            TextString   = Fore.RESET + 20*' '
            PVmin        = 0.5 * PVmin
            if SoLo_Bezug >=  PVmin :       # nur einschalten , wenn ausreichender PV-Ertrag
                Schalter     = True
                TextString      = TextString + '(Einspeisung für Garten ausreichend ' + str(SoLo_Bezug) + ' >= 1/2 PVmin ' + str(PVmin) + ')'
            else :
                Schalter     = False
                if SoLo_Bezug >= 0 :
                    TextString  = TextString + '(Einspeisung für Garten nicht ausreichend ' + str(SoLo_Bezug) + ' < 1/2 PVmin ' + str(PVmin) + ')'
                else :
                    TextString  = TextString + '(Einspeisung für Garten nicht ausreichend , da Bezug negativ ' + str(SoLo_Bezug) + ')'
            # Schaltvorgang durchführen
            print (Func_Relais.Set (RELAIS , Schalter , drucken , loggen))
            print (TextString)
            time.sleep(1)                   # 1 sec warten
        
        #  keine Sonstige --> alle Relais ausschalten , die davon betroffen sind !   
        else :
            TextString = Fore.YELLOW + 'Sonstige            und zugehörige Relais WK3,GK1 ausgeschaltet' + Style.RESET_ALL 
            print (TextString)
            # Schaltvorgang aus durchführen
            Schalter         = False
            drucken          = False
            RELAIS = 'WK3'   # ping-Relais
            TextString = (Func_Relais.Set (RELAIS , Schalter  , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten
            RELAIS = 'GK1'   # Garten-Relais
            TextString = (Func_Relais.Set (RELAIS , Schalter  , drucken , loggen))
            if TextString != () : print (TextString)
            time.sleep(1)                   # 1 sec warten   
        # Ende Schaltvorgänge #######################################################################################
        if not Tagsteuerung : wait = wait * NachtFaktor # in der Nacht verlängerter Zyklus
        if iverarb == 1   : wait = wait / 2             # beim 1. Lauf nur 1/2 Zeit warten
        TextString = ' ENDE Entladesteuerung     ' + str(iverarb + 1) + '. Lauf beginnt in ' + str(wait) + ' Sekunden ----------------'
        TextString = time.strftime("%Y.%m.%d %H:%M:%S") + TextString
        print (Fore.GREEN + TextString)
        
        # Ende Endlosschleife nächster Lauf zyklisch nach x Sekunden
        print ()
        time.sleep(wait)
    # while(true) Block Ende

except KeyboardInterrupt as e :
    # Programm beendet mit CTRL+C oder Strg+C
    print ()
    END_TEXT   = 'ENDE Entladesteuerung ' + Version
    END_TEXT1  = 'mit KeyboardInterrupt (CTRL+C oder Strg+C)'
    END_TEXTZ  = Fore.GREEN + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + ' '
    END_TEXTZ1 = Fore.GREEN + Style.BRIGHT + 20 * ' '
    print   (END_TEXTZ  + END_TEXT)                     # 1. Zeile Drucken           
    print   (END_TEXTZ1 + END_TEXT1)                    # 2. Zeile Drucken
    Logsatz (END_TEXT , True)                           # 1. Zeile Loggen und Drucken
    Logsatz (END_TEXT1, False)                          # 2. Zeile Loggen , nicht Drucken  
    END_TEXT = ''                                       # weiter zum Ende --> finally
    
except AssertionError as e :
    # Programm ABBRUCH mit AssertionError
    print ()
    END_TEXT   = 'ABBRUCH Entladesteuerung ' + Version
    END_TEXT1  = 'mit AssertionError : '
    END_TEXT2  = str(e)
        
except Exception as e :
    # Programm ABBRUCH mit Exception
    print ()
    END_TEXT   = 'ABBRUCH Entladesteuerung ' + Version
    END_TEXT1  = 'mit Exception : '
    END_TEXT2  = str(e)

finally :
    # Das Programm wird hier beendet
    if END_TEXT == '' :                                     # ordnungsgemäß beendet
        print ()
        END_TEXT = 20 * ' ' + '---> Programm fehlerfrei beendet und' 
        print (Fore.GREEN + Style.BRIGHT + END_TEXT )
    else :                                                  # Abbruch mit Assertion oder Exception
        END_TEXTZ  = Fore.RED + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + ' '
        END_TEXTZ1 = Fore.RED + Style.BRIGHT + 20 * ' '
        print   (END_TEXTZ  + END_TEXT)                     # 1. Zeile Drucken           
        print   (END_TEXTZ1 + END_TEXT1)                    # 2. Zeile Drucken
        print   (END_TEXTZ1 + END_TEXT2)                    # 3. Zeile Drucken
        Logsatz (END_TEXT, True)                            # 1. Zeile Loggen und Drucken
        Logsatz (END_TEXT1, False)                          # 2. Zeile Loggen , nicht Drucken
        Logsatz (END_TEXT2, False)                          # 3. Zeile Loggen , nicht Drucken       
    # Initialisierung / Reset aller Relais
    # Setzen Parameter zur Initialisierung aller Relais
    drucken      = True           # True = ja , False = nein
    loggen       = 'RelTab'       # aus RelTab ober True = ja , False = nein
    RELAIS       = 'alle'         # alle Relais wie in Relais-Tabelle GVS.RelTab() definiert
    # Initialisierung durchführen Reset , ggf.Ergebnis drucken , loggen
    Schalter     = False         # True = ein , False = aus
    print (Func_Relais.Reset (RELAIS , Schalter , drucken , loggen))
    
#   sys.exit(0)  # wenn kein Fehler in die Console geschrieben werden soll
