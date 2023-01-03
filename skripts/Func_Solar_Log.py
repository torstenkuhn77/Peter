#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Auslesen von Daten über JSON Schnittstelle des Solar-Log
# siehe hier : https://constey.de/2014/10/solarlog-200-momentanwerte-per-kommandozeile-auslesen/

import json
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import GVS          # eigene globale Variablen

from colorama import init , Fore , Style
                    # init(autoreset=True) Farbe gilt nur je Printposition
                    # init()               Farbe gilt bis Programmende
                    #Farben :
                    #Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Style: DIM, NORMAL, BRIGHT, RESET_ALL

init(autoreset=True)


#   Beschreibung Solar-Log JSON Schnittstellendaten : ##################
#   100 - LastUpdateTime
#   101 - W Pac (Gesamtleistung) aller Zähler & WR
#   102 - W Pdc (Gestamtleistung aller WR)
#   103 - V Uac Durchschnittliche Spannung UAC der Wechselrichter
#   104 - V Durchschnittliche Spannung UDC der Wechselrichter
#   105 - Wh Durchschnittliche Spannung UDC der Wechselrichter
#   106 - Wh Summierter gestriger Tagesertrag aller Wechselrichter
#   107 - Wh Summiertes Monatsertrag aller WR
#   108 - Wh Summiertes Jahresertrag aller WR
#   109 - Wh Gesamtertrag aller Wechselrichter
#   110 - W momentaner Gesamtverbrauch PAC aller Verbauchszähler
#   111 - Wh Summierter Verbrauch aller Verbauchs-zähler
#   112 - Wh Summierter Verbrauch des gestrigen Tages; alle Verbauchszähler
#   113 - Wh Summierter Verbrauch des Monats; alle Verbauchszähler
#   114 - Wh Summierter Verbrauch des Jahres, alle Verbauchszähler
#   115 - Wh Summierter Gesamtverbrauch, alle Ver-bauchszähler
#   116 - Wp Installierte Generatorleistung


def Lesen (localIP) :

    Text = 'PV Solar-Log        '
    
    req = Request("http://" + localIP)

    try:# URLError, HTTPError abfangen
        response = urlopen(req)
    except HTTPError as e:
        # keine HTTP-Verbindung zum Solar-Log
        Text = Text + Fore.YELLOW + 'keine HTTP-Verbindung HTTPError code: '+ str(e.code)
    except URLError  as e:
        # keine LAN-Verbindung zum Solar-Log
        Text = Text + Fore.YELLOW + 'keine LAN-Verbindung URLError Reason: '+ str(e.reason)
    else:
        # Daten vom Solar-Log einlesen und verarbeiten
        # update der JSON-Schnittstelle erfolgt alle 15 sec,
        
        req = urllib.request.Request('http://'+ localIP +'/getjp')
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        data = '{"801":{"170":null }}'
        jd = json.dumps(data)
        jb = jd.encode('utf-8')

        req.add_header('Content-Length', len(jb))

        response = urllib.request.urlopen(req, jb)
        if (response.getcode()== 200):
            cb = response.read()
            s = cb.decode('ascii')     
               
            # konvertiert die gelesenen bytes in einen json string
            current = json.loads(s)
            
            lut    = current["801"]["170"]["100"]         # last update time dd.mm.yy hh.mm.ss
            if lut == "ACCESS DENIED" :
                Text = Text + Fore.YELLOW + "Zugriff auf JSON Schnittstelle verweigert" + Fore.RESET
            else :
                day    = lut[0:2]                         # Konvertierung zum üblichen timestamp
                month  = lut[3:5]
                year   = lut[6:8]
                rest   = lut[8:17]
                lut    = '20'+year+'.'+month+'.'+day+rest  # last update time yyyy.mm.dd hh.mm.ss
                
                GVS.SolarLog_Verbrauch = round(current["801"]["170"]["110"]/ 1000 ,2)  # update globale Variablen in GVS
                GVS.SolarLog_Erzeugung = round(current["801"]["170"]["101"]/ 1000 ,2)
                Bezug                  = (round((GVS.SolarLog_Erzeugung - GVS.SolarLog_Verbrauch),2))
                Text = Text + "Verbrauch " + Fore.RED + str(GVS.SolarLog_Verbrauch) + Fore.RESET
                Text = Text + " Erzeugung " + Fore.YELLOW + str(GVS.SolarLog_Erzeugung) + Fore.RESET
                if Bezug >= 0 :
                    Text = Text + " Einspeisung " + Fore.GREEN + str(Bezug)
                else :
                    Text = Text + " Bezug " + Fore.RED + str(Bezug) 
                
                Text = Text + Style.RESET_ALL + ' KW ' + '(' + lut + ')'                            
        else:
            Text = Text + Fore.YELLOW + "Fehler beim Lesen JSON Schnittstelle "+ response.getcode() + Fore.RESET

    return (Text)

