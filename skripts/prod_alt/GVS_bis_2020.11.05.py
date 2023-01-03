#!/usr/bin/python3
# -*- coding: utf-8 -*-

# GVS : Global Variable Storage  ############################################################
# hier sind alle Variablen gesoeichert , verwendet in und zwischen
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

# Dictionary Relais-Tabelle gültiger und verdrahteter Relais mit GPIO , PIN , Funktionsbezeichnung
RelTab = {
    "WK1"       : 12,    # PIN 32 RPI Farbe orange
    "WK1_Funk"  : 'Tagbetrieb                             ',
    "WK2"       : 16,    # PIN 36 RPI Farbe blau
    "WK2_Funk"  : 'boost (Mischer öffnen)                 ',
    "WK3"       : 20,    # PIN 38 RPI Farbe braun
    "WK3_Funk"  : 'ping Funktemperaturstation TFA 3035    ',
    "WK4"       : 00,    # PIN 40 RPI Farbe grün
    "WK4_Funk"  : 'unbenutztes Relais Wohnzimmer          ',
    "GK1"       : 21,    # PIN 40 RPI Farbe grün
    "GK1_Funk"  : 'Garten                                 ',
    "KK1"       : 19,    # PIN 35 RPI Farbe weiß
    "KK1_Funk"  : 'Boiler Nacht(BK1)- / Direktladung(DK1) ',
    "BK1"       : 19,    # PIN 35
    "BK1_Funk"  : 'Boiler Nachttarif-Ladung noch im Test  ',
    "DK1"       : 19,    # PIN 35
    "DK1_Funk"  : 'Boiler Direkt-Ladung     noch im Test  ',
    "DK1_Hist"  : False, # Histerese Schalter Boiler Direkt-Ladung initial aus
    "KK2"       : 26,    # PIN 37 RPI Farbe gelb
    "KK2_Funk"  : 'Kessel Nacht(HK2)- / Direktladung(DK2) ',
    "HK2"       : 26,    # PIN 37
    "HK2_Funk"  : 'Kessel Nachttarif-Ladung noch im Test  ',
    "DK2"       : 26,    # PIN 37
    "DK2_Funk"  : 'Kessel Direkt-Ladung     noch im Test  ',
    "DK2_Hist"  : False  # Histerese Schalter Kessel Direkt-Ladung initial aus
         }

# LogDatei für Relaissteuerung
RelLogDir  = '/home/pi/skripts/prod'
RelLogFile = 'Log_Relais.txt'



