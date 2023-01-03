#!/usr/bin/python3
# -*- coding: utf-8 -*-

# GVS : global variable storage
# https://www.programiz.com/python-programming/global-keyword
# dort : Example 4 : Share a global Variable Across Python Modules

# Variablen für Übergabe an bzw. aus Solar-Log
SolarLog_Verbrauch = 0
SolarLog_Erzeugung = 0

# Variablen für Prüfung ob NT-Ladung
NT_Ladung_Geraet = False

# Dictionary Relais-Tabelle gültiger und verdrahteter Relais mit GPIO und Funktionsbezeichnung
RelTab = {
          "WK1"       : 12,
          "WK1_Funk"  : ' Tagbetrieb                          ',
          "WK2"       : 16,
          "WK2_Funk"  : ' boost                               ',
          "WK3"       : 20,
          "WK3_Funk"  : ' ping Funktemperaturstation TFA 3035 ',
          "WK4"       : 21,
          "WK4_Funk"  : ' ping Test unbenutztes Relais        ',
          "BK1"       : 19,
          "BK1_Funk"  : ' Boiler NT-Ladung noch im Test       ',
          "HK2"       : 26,
          "HK2_Funk"  : ' Kessel NT-Ladung noch im Test       '
          }

# LogDatei für Relaissteuerung
RelLogDir  = '/home/pi/skripts/prod'
RelLogFile = 'Log_Relais.txt'



