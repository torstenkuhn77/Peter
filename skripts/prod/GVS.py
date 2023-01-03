#!/usr/bin/python3
# -*- coding: utf-8 -*-

# GVS : Global Variable Storage  ############################################################
# hier sind alle Variablen gespeichert , verwendet in und zwischen
# Programmen , Programmteilen oder Programmläufen
# Beispiel :
# https://www.programiz.com/python-programming/global-keyword
# dort : Example 4 : Share a global Variable Across Python Modules
#############################################################################################


# Variablen für Übergabe an bzw. aus Solar-Log
# lokale fixe IPV4 Adresse :
# 169.254.xx.yy letzte 4 Stellen = letzte 4 Stellen der SN des Solar-Log
# hier Seriennummer 1350323432 --> 169.254.34.32
# alternativ DHCP-Adresse aus dem lokalen Netzwerk verwenden
SolarLog_localIP   = '169.254.34.32'           # lokale IP des Solar-Log
# initial o , falls Zugriff auf Schnittstelle nicht erfolgreich
SolarLog_Verbrauch = 0
SolarLog_Erzeugung = 0

# Dictionary Relais-Tabelle gültiger und verdrahteter Relais und GPIOs / PINs
# mit GPIO , PIN , Log-Schalter , Funktionsbezeichnung , ggf. Histerese-Schalter
RelList = ['WK1','WK2','WK3','WK4','GK1','KK1','KK2']
# zu jedem in dieser Liste aufgeführten Relais muß ein Datensatz in folgender Tabelle vorhanden sein !
# aber nur solche , die physisch an Relais angeschlossen sind
# also nicht BK1,DK1 , HK2,DK2 , one-wire 
RelTab = {
    ##### Wohnzimmer Relais WK1 (physisch) #################################
    "WK1"       : 12,    # PIN 32 RPI Farbe orange
    "WK1_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "WK1_Funk"  : 'Tagbetrieb                             ',
    ##### Wohnzimmer Relais WK2 (physisch) #################################
    "WK2"       : 16,    # PIN 36 RPI Farbe blau
    "WK2_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "WK2_Funk"  : 'boost (Mischer öffnen)                 ',
    ##### Wohnzimmer Relais WK3 (physisch) #################################
    "WK3"       : 20,    # PIN 38 RPI Farbe braun
    "WK3_Log"   : False, # True = Ja,Logsatz  False = Nein 
    "WK3_Funk"  : 'ping Funktemperaturstation TFA 3035    ',
    ##### Wohnzimmer Relais WK4 (physisch) #################################
    "WK4"       : 13,    # PIN 33 RPI Farbe grau reserviert für Unterbrechung ONE-Wire Bus
    "WK4_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "WK4_Funk"  : 'Unterbrechung ONE-Wire Bus             ',
    ##### Keller Relais GK1 (physisch) #####################################
    "GK1"       : 21,    # PIN 40 RPI Farbe grün
    "GK1_Log"   : False, # True = Ja,Logsatz  False = Nein 
    "GK1_Funk"  : 'Garten                                 ',
    ##### Keller Relais KK1 (physisch) und zugehörige BK1,DK1 (logisch) ####
    "KK1"       : 19,    # PIN 35 RPI Farbe weiß
    "KK1_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "KK1_Funk"  : 'Boiler Nacht(BK1)- / Direktladung(DK1) ',
    "BK1"       : 19,    # PIN 35
    "BK1_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "BK1_Funk"  : 'Boiler Nachttarif-Ladung               ',
    "DK1"       : 19,    # PIN 35
    "DK1_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "DK1_Funk"  : 'Boiler Direkt-Ladung                   ',
    "DK1_Hist"  : False, # Histerese Schalter Boiler Direkt-Ladung initial aus
    ##### Keller Relais KK2 (physisch) und zugehörige HK2,DK2 (logisch) #######
    "KK2"       : 26,    # PIN 37 RPI Farbe gelb
    "KK2_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "KK2_Funk"  : 'Kessel Nacht(HK2)- / Direktladung(DK2) ',
    "HK2"       : 26,    # PIN 37
    "HK2_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "HK2_Funk"  : 'Kessel Nachttarif-Ladung               ',
    "DK2"       : 26,    # PIN 37
    "DK2_Log"   : True,  # True = Ja,Logsatz  False = Nein 
    "DK2_Funk"  : 'Kessel Direkt-Ladung                   ',
    "DK2_Hist"  : False, # Histerese Schalter Kessel Direkt-Ladung initial aus
    ##### one-wire bus , kein Relais physisch vorhanden #######################
    "one-wire"  : 4,     # PIN  7 RPI Farbe gelb
    "o-w_Funk"  : 'one-wire bus , nicht geschaltet !!!    '
         }

# LogDatei für Relaissteuerung
RelLogDir  = '/home/pi/skripts/prod'
RelLogFile = 'Log_Relais.txt'

# Dictionary Temperaturensensoren-Tabelle Typ DS18B20
# mit Bezeichnung , Schlüssel/Ort im Systembus , Wert und timestamp der zuletzt ausgelesenen Temperatur ,
# Korrektur des ausgelesenen Wertes
# zum Auslesen der Sensoren/Schlüssel siehe skript  /home/pi/Desktop/skripts/Liste der Sensoren.py 
# l = [K2_Rel , K2_Schalter]
void_key = 'void'                                   # Dieser Sensor wird nicht berücksichtigt , da Platzhalter
SensTypList  = ['DS18B20']                          # gültige Sensoren - Typen ohne Platzhalter (void)
SensList     = ['Raum','Kessel','unten','Vorlauf','Boiler'] # gültige Temperatur-Sensoren vom Typ ...
# zu jedem in dieser Liste aufgeführten Sensor muß ein Datensatz in folgender Tabelle vorhanden sein !
SensTab = {
    "Raum"       : '/sys/bus/w1/devices/w1_bus_master1/28-01186c88d8ff/w1_slave', # Sensorbezeichnung Raum neu 25.12.2020
    "Raum_Typ"   : 'DS18B20',                                                     # Sensortyp
    "Raum_Tmp"   : 0.0,                                                           # letzte Temperatur
    "Raum_Stp"   : '00.00.0000 00:00:00',                                         # timestamp letzte Temp oder Lesefehler
    "Raum_Kor"   : 0.0,                                                           # Raumkorrektur
    ############################################################################### Ende Sensor Raum    
    "Kessel"     : '/sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave', # Sensorbezeichnung Kessel oben
    "Kessel_Typ" : 'DS18B20',                                                     # Sensortyp
    "Kessel_Tmp" : 0.0,                                                           # letzte Temperatur
    "Kessel_Stp" : '00.00.0000 00:00:00',                                         # timestamp letzte Temp oder Lesefehler
    "Kessel_Kor" : 0.0,                                                           # Kesselkorrektur oben
    ############################################################################### Ende Kessel oben
    "unten"      : '/sys/bus/w1/devices/w1_bus_master1/28-0309977914a4/w1_slave', # Sensorbezeichnung Kessel unten
    "unten_Typ"  : 'DS18B20',                                                     # Sensortyp
    "unten_Tmp"  : 0.0,                                                           # letzte Temperatur
    "unten_Stp"  : '00.00.0000 00:00:00',                                         # timestamp letzte Temp oder Lesefehler
    "unten_Kor"  : 0.0,                                                           # Kesselkorrektur unten
    ############################################################################### Ende Kessel unten
    "Vorlauf"    : '/sys/bus/w1/devices/w1_bus_master1/28-030997790e32/w1_slave', # Sensorbezeichnung Vorlauf
    "Vorlauf_Typ": 'DS18B20',                                                     # Sensortyp
    "Vorlauf_Tmp": 0.0,                                                           # letzte Temperatur
    "Vorlauf_Stp": '00.00.0000 00:00:00',                                         # timestamp letzte Temp oder Lesefehler
    "Vorlauf_Kor": 4.1,                                                           # Vorlaufkorrekturtur
    ############################################################################### Ende Sensor Vorlauf
    "Boiler"     : '/sys/bus/w1/devices/w1_bus_master1/28-0316a27937aa/w1_slave', # Sensorbezeichnung Boiler
    "Boiler_Typ" : 'DS18B20',                                                     # Sensortyp
    "Boiler_Tmp" : 0.0,                                                           # letzte Temperatur
    "Boiler_Stp" : '00.00.0000 00:00:00',                                         # timestamp letzte Temp oder Lesefehler
    "Boiler_Kor" : 5.1,                                                           # Boilerkorrektur
    ############################################################################### Ende Sensor Boiler
    "void"    : 'void - als Platzhalter für weitere Sensoren ------------------', # Platzhalter für weitere Sensoren
    "void_Typ": 'void',                                                           # Sensortyp
    "void_Tmp": 0.0,                                                              # letzte Temperatur
    "void_Stp": '00.00.0000 00:00:00',                                            # timestamp letzte Temp oder Lesefehler
    "void_Kor": 0.0                                                               # Korrekturwert Sensor
    ############################################################################### Ende Platzhalter
          }