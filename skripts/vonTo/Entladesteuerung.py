# Steuerungsparameter definieren ,setzen , protokollieren

import time , sys , RPi.GPIO as GPIO
import Temp_Sens_Abfrage , Func_Relais

try:
    while True :
        
        print ()
        print (time.strftime("%d.%m.%Y %H:%M:%S") ,"START Entladesteuerung  --------------------------------")
        print ("Steuerungsparameter,aktuelle Werte : (Zeiten hh:mm , Temperaturen Grad Celsius)")

        # Tagsteuerung von bis
        DTvon = "08:30"
        DTbis = "16:30"
        DTakt = time.strftime("%H:%M")
        if DTakt >= DTvon and DTakt <= DTbis :
            Tagsteuerung = True
            print ("Tagbetrieb        von",DTvon,"bis",DTbis,'aktuell',DTakt,'-->  aktiv')
        else :
            Tagsteuerung = False
            print ("Nachtbetrieb      von",DTbis,"bis",DTvon,'aktuell',DTakt,'-->  aktiv')

        # Nachtaufladung von bis
        NAvon = "22:15"
        NAbis = "05:45"
        if Tagsteuerung == False and DTakt >= NAvon or DTakt <= NAbis :
            Nachtaufladung = True
            print ("Nachtaufladung    von",NAvon,"bis",NAbis,'aktuell',DTakt,'-->  aktiv')
        else :
            Nachtaufladung = False
            print ("Nachtaufladung    von",NAvon,"bis",NAbis,'aktuell',DTakt,'-->  nicht aktiv')
        
        
        # Raumtemperatur , aktuell, max
        # Sensor 28-0309977914a4
        sensorRT = Temp_Sens_Abfrage.sensorRT
        RTakt = Temp_Sens_Abfrage.readTempLines(sensorRT)[0]
        RTmax =   24.0
        print ("Raumtemperatur    aktuell",RTakt,"max",RTmax)

        # Boilertemperatur  aktuell . min , max
        # Sensor 
        sensorBT = Temp_Sens_Abfrage.sensorBT
        BTakt =   Temp_Sens_Abfrage.readTempLines(sensorBT)[0]
        BTmin =   45.0
        BTmax =   65.0
        print ("Boilertemperatur  aktuell",BTakt,"max",BTmax,"min",BTmin)
        
        # Vorlauftemperatur , aktuell , max
        # Sensor 28-030997790e32
        sensorVT = Temp_Sens_Abfrage.sensorVT
        VTakt = Temp_Sens_Abfrage.readTempLines(sensorVT)[0]
        VTmax =   35.0
        print ("Vorlauftemperatur aktuell",VTakt,"max",VTmax)
        
        
        # Kesseltemperatur aktuell , min , max , boost
        # Sensor 28-030997790a01
        sensorKT = Temp_Sens_Abfrage.sensorKT
        KTakt = Temp_Sens_Abfrage.readTempLines(sensorKT)[0]
        KTmin =   40.0
        KTmax =   75.0
        KTboost = 65.0
        # Beginn boost erst 1 Stunde nach Beginn der Tagsteuerung
        i1 = DTvon [0]
        i2 = DTvon [1]
        i3bis5 = DTvon [2] + DTvon [3] + DTvon [4]
        i2 = int (i2) + 1
        i2 = str (i2)
        boostfrom = i1 + i2 + i3bis5
        # 1 Stelle nach links schieben , wenn hh 2-stellig
        if boostfrom [0] == '0' and len(boostfrom) >= 6 :
            boostfrom = boostfrom[1] + boostfrom[2] + boostfrom[3] + boostfrom[4] + boostfrom[5]
        if boostfrom > '22:59' :
            print ('Fehler bei Angabe der Tagzeit',DTvon,'--> boost Zeit ',boostfrom)
        
        print ("Kesseltemperatur  aktuell",KTakt,"max",KTmax,"min",KTmin,'boost möglich ab',boostfrom,'bei',KTboost)
        if Tagsteuerung == False :
            boost = False
            print         ('                  boost nicht aktiv , da Nachtbetrieb')
        else :
            if KTakt >= KTboost and VTakt <= VTmax and RTakt <= RTmax and DTakt >= boostfrom :
                boost = True
                print     ('                  boost möglich','seit',boostfrom)
            else :
                boost = False
                if KTakt < KTboost :
                    print ('                  boost nicht aktiv weil Kesseltemperatur  zu niedrig')
                if VTakt > VTmax :
                    print ('                  boost nicht aktiv weil Vorlauftemperatur zu hoch')
                if RTakt > RTmax :
                    print ('                  boost nicht aktiv weil Raumtemperatur    zu hoch')
                if DTakt < boostfrom :
                    print ('                  boost nicht aktiv weil erst ab',boostfrom,'verfügbar')
                
                
        # Beginn Verarbeitung
        print ('Start Verarbeitung :')
        
        # Setzen Parameter zur Schaltung von Relais für die Funktio na-/Nachtbetrieb
        RELAIS       = 'WK1'
        RELAIS_GPIO  =  12
        # Schaltvorgang durchführen
        if Tagsteuerung :
            Funktion     = ' Tagbetrieb'
            Schalter     = 'ein'   # zulässig : ein , aus , tip
            Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter)
        else :
            Funktion     = ' Tagbetrieb'
            Schalter     = 'aus'   # zulässig : ein , aus , tip
            Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter)

        # Setzen Parameter zur Schaltung von Relais für die Funktion boost
        RELAIS       = 'WK2'
        RELAIS_GPIO  =  16
        # Schaltvorgang durchführen
        if boost :
            Funktion     = ' boost'
            Schalter     = 'ein'   # zulässig : ein , aus , tip
            Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter)
        else :
            Funktion     = ' boost'
            Schalter     = 'aus'   # zulässig : ein , aus , tip
            Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter)

        # Setzen Parameter zur Schaltung von Relais für die Funktion TFA 3035
        Funktion     = ' Funktemperaturstation TFA 3035'
        RELAIS       = 'WK3'
        RELAIS_GPIO  =  20
        Schalter     = 'ping'   # zulässig : ein , aus , ping
        # Schaltvorgang durchführen
        Func_Relais.Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter)
        
        # Ende Verarbeitung
        print (time.strftime("%d.%m.%Y %H:%M:%S") ,
               'Ende Verarbeitung Entladesteuerung  ----------------------')

        # Programmende
        time.sleep(60)   # nächster Lauf nach x Sekunden
        
        
except KeyboardInterrupt:
    # Programm beendet mit CTRL+C
    print      (time.strftime("%d.%m.%Y %H:%M:%S") ,
                'ENDE Entladesteuerung beendet mit CTRL+C / Strg+C  -------')
    GPIO.cleanup()
    
except Exception as e:
    print(str(e))
    sys.exit(1)

finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    print       (time.strftime("%d.%m.%Y %H:%M:%S") ,
                 'Programm Entladesteuerung beendet  -----------------------')
    GPIO.cleanup()
    sys.exit(0)

