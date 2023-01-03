# shell : python3 /home/pi/skripts/prod/Func_Sens.py

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Problem :
# 2020.11.08 12:17:29 ENDE Entladesteuerung mit AssertionError :
#                     ('Fehler im Skript "Func_Sens.Temp" : beim Auslesen des Sensors ', 'Vorlauf', ' im Systembus ', '', '')

# 2020.11.09 01:34:12 ENDE Entladesteuerung mit AssertionError :
#                     ('Fehler im Skript "Func_Sens.Temp" : beim Auslesen des Sensors ', 'Raum', ' im Systembus ', '', '')

# 2020.11.09 04:44:59 ENDE Entladesteuerung mit Exception :
#                     [Errno 2] No such file or directory: '/sys/bus/w1/devices/w1_bus_master1/28-0309977914a4/w1_slave'


import GVS      # Zwischenspeicher eigene globale Variablen

def Temp(Bez) : # Aus Systembus Temperatursensoren DS18B20 auslesen
    
    if Bez not in GVS.SensTab.keys() :
        return ('Fehler im Skript "Func_Sens.Temp" : "' + Bez + '" nicht in der Tabelle der Temperatursensoren')  
    else :   
        # Aus Systembus Temperatursensoren DS18B20 auslesen
        Ort = str(GVS.SensTab.get (Bez))
        Korrektur = float(GVS.SensTab.get (Bez + '_Kor'))
        f = open(Ort, 'r')
        line1 = f.readline()               # 1. Zeile lesen
        line2 = f.readline()               # 2. Zeile lesen
        f.close()
        # Position von t=..... in der 2. Zeile finden
        temperaturStr = line2.find('t=')   # t=..... finden
        if temperaturStr != -1 :           # not equal -1 --> Temperatur kann ausgelesen werden
            tempData = line2[temperaturStr+2:]
            # auf 1 Nachkommastelle runden
            tempCelsius   = round(float(tempData) / 1000,1)
            tempCelsius_r = round(tempCelsius + Korrektur ,1)
            
#             # aktivieren für Testzwecke : ######################################
#             print ()
#             print ('Skript "Func_Sens.Temp" , ausgelesen wurde : ')
#             print ()
#             print ('Sensor                 : ',Bez,Ort)
#             print ()
#             print ('1. Zeile               : ',line1)
#             print ('2. Zeile               : ',line2)
#             print ('Temp-String Position   : ',temperaturStr)
#             print ()
#             print ('Temp-String Wert       : ',tempData)
#             print ('Temperatur gerundet    : ',tempCelsius)      
#             print ()
#             print ('Korrekturwert          : ',Korrektur)
#             print ()
#             #########################################################
            
            return (tempCelsius_r)
            
        else :
            return ('Fehler im Skript "Func_Sens.Temp" : beim Auslesen des Sensors ', Bez , ' im Systembus ',line1,line2)
                    