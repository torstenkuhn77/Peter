# shell : python3 /home/pi/skripts/vonTo/ReadSolarLog.py
# Auslesen von Daten über JSON Schnittstelle des Solar-Log
# siehe hier : https://constey.de/2014/10/solarlog-200-momentanwerte-per-kommandozeile-auslesen/

import json
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

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

# lokale IPV4 Adresse : 169.254.xx.yy letzte 4 Stellen = letzte 4 Stellen der SN des Solar-Log
# hier Seriennummer 1350323432 --> 169.254.34.32
# alternativ DHCP-Adresse aus dem lokalen Netzwerk verwenden

localIP = "169.254.34.32"
req = Request("http://" + localIP)

try:# URLError, HTTPError abfangen
    response = urlopen(req)
except HTTPError as e:
    # keine HTTP-Verbindung zum Solar-Log
    print ('PV Solar-Log : keine HTTP-Verbindung HTTPError code: ', e.code)
except URLError  as e:
    # keine LAN-Verbindung zum Solar-Log
    print ('PV Solar-Log : keine LAN-Verbindung URLError Reason: ', e.reason)
else:
    # Daten vom Solar-Log einlesen und verarbeiten
    print ('PV Solar-Log : Verbindung hergestellt')

    req = urllib.request.Request('http://'+ localIP +'/getjp')
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    data = '{"801":{"170":null }}'
    jd = json.dumps(data)
    jb = jd.encode('utf-8')

    req.add_header('Content-Length', len(jb))

    response = urllib.request.urlopen(req, jb)
    if (response.getcode()== 200):
        cb = response.read()
            
        print ('PV Solar-Log : asci-code Ausgabe')
        s = cb.decode('ascii')   
        print (s)
        print ()
        
        # konvertiert die gelesenen bytes in einen json string
        current = json.loads(s)
        # pretty print
        print ('PV Solar-Log : JSON-string Ausgabe , je 4 Stellen versetzt')
        print (json.dumps(current, indent = 4))
        
        lut    = current["801"]["170"]["100"]         # last update time dd.mm.yy hh.mm.ss
        if lut == "ACCESS DENIED" :
            print ("PV Solar-Log  : Zugriff auf JSON Schnittstelle verweigert")
        else :
            day    = lut[0:2]                          # Konvertierung zum üblichen timestamp
            month  = lut[3:5]
            year   = lut[6:8]
            rest   = lut[8:17]
            lut    = '20'+year+'.'+month+'.'+day+rest  # last update time yyyy.mm.dd hh.mm.ss
            
            Verbrauch = round(current["801"]["170"]["110"]/ 1000 ,2)
            Erzeugung = round(current["801"]["170"]["101"]/ 1000 ,2)
            Bezug     = (round((Erzeugung - Verbrauch),2))
            if Bezug >= 0 :
                print (lut,"PV Solar-Log : Erzeugung", Erzeugung ,"Verbrauch" , Verbrauch ,"Einspeisung" , Bezug , 'KW')
            else :
                print (lut,"PV Solar-Log : Erzeugung", Erzeugung ,"Verbrauch" , Verbrauch ,"Bezug" , Bezug , 'KW')
    else:
        print ("PV Solar-Log : Fehler beim Lesen JSON Schnittstelle", response.getcode())
