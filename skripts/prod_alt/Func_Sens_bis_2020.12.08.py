# shell : python3 /home/pi/skripts/prod/Func_Sens.py

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

import GVS      # Zwischenspeicher eigene globale Variablen

def Temp(Bez) : # Aus Systembus einen einzelnen Temperatursensor DS18B20 auslesen

    if Bez not in GVS.SensTab.keys() :
        return ('Fehler im Skript "Func_Sens.Temp" : "' + Bez +
                '" nicht in Tabelle Temperatursensoren (GVS.SensTab)')
    if Bez not in GVS.SensList :
        return ('Fehler im Skript "Func_Sens.Temp" : "' + Bez +
                '" nicht in Liste Temperatursensoren (GVS.SensList)')
    else :   
        # Aus Systembus Temperatursensoren DS18B20 auslesen
        line1und2 = LesBus (str(GVS.SensTab.get(Bez))) # Liste füllen

#         # für Testzwecke : ######################################
#         print ('Ergebnis nach dem Lesen im Systembus :')
#         print ()
#         #########################################################

        line1 = line1und2.pop(0)                       # Liste entladen       
        line2 = line1und2.pop(0)

#         # für Testzwecke : ######################################
#         print ('1. Zeile : ',line1)
#         print ('2. Zeile : ',line2)
#         #########################################################

        if 'Fehler' in line1 : # Abbruch bei Lesefehler im Systembus
            return (line1,line2)
        else :
            # Position von t=..... in der 2. Zeile finden
            temperaturStr = line2.find('t=')   # t=..... finden
            tempData = line2[temperaturStr+2:]
            # auf 1 Nachkommastelle runden
            tempCelsius   = round(float(tempData) / 1000,1)
            # Korrekturwert des Sensord dazu addieren
            tempCelsius_r = round(tempCelsius +
                            float(str(GVS.SensTab.get(Bez + '_Kor'))) ,1)
            
#             # für Testzwecke : ######################################
#             print ()
#             print ('Skript "Func_Sens.Temp" , ausgelesen wurde : ')
#             print ()
#             print ('Sensor                 : ',Bez,str(GVS.SensTab.get(Bez)))
#             print ()
#             print ('1. Zeile               : ',line1)
#             print ('2. Zeile               : ',line2)
#             print ('Temp-String Position   : ',temperaturStr)
#             print ()
#             print ('Temp-String Wert       : ',tempData)
#             print ('Temperatur gerundet    : ',tempCelsius)      
#             print ()
#             print ('Korrekturwert          : ',GVS.SensTab.get(Bez + '_Kor'))
#             print ()
#             #########################################################
            
            return (tempCelsius_r)


def LesBus(Index) :                # Systembus lesen
    line1     =''                  # Initialisierung
    line2     = ''
    line1und2 = [line1,line2]
    i         = 0
    imax      = 2
    iwait     = 0.5                 # Sek. warten bei Iteration
        
    # Lesen , ggf. Nachlesen , falls keine Temperatur gefunden
    while 'YES' not in line1 or 't=' not in line2 :
        i = i + 1
        if i > 1 : time.sleep (iwait) # mit Nachlesen warten !
        try :
            f = open(Index, 'r')
        except IOError  :            # Abbruch , da Nachlesen erfolglos
            line1 = 'Fehler im Skript Func_Sens.Temp.LesBus'
            line2 = Index + ' one-wire bus konte nicht ausgelesen werden ' 
            line1und2 =[line1,line2]
            return (line1und2)        # Rückgabe Fehler
        line1 = f.readline()          # 1. Zeile lesen
        line2 = f.readline()          # 2. Zeile lesen
        line1und2 = [line1,line2]     # Liste erstellen
        f.close()
        if i > 1 :
            print (Index,' gelesen im Systembus nach ',str(i),'Iterationen : ')
            print ('1. Zeile : ',line1,' 2. Zeile : ',line2) 
        if i > imax :                 # Abbruch , da Nachlesen erfolglos
            line1 = 'Fehler im Skript Func_Sens.Temp.LesBus'
            line2 = str(imax) + ' Iterationen überschritten' 
            line1und2 =[line1,line2]
            return (line1und2)        # Rückgabe Fehler
    
#     # für Testzwecke : #########################################
#     print ('gelesen im Systembus nach ',str(i),'Iterationen : ')
#     print ('1. Zeile : ',line1)
#     print ('2. Zeile : ',line2)
#     ############################################################
    
    return (line1und2)                 # Ergebnis als Liste zurückgeben

# # für Testzwecke :  #############################################
# print (80 *'-')
# Sensor = ('Raum')   # gültiger  Sensor
# print ('Test mit Sensor ',Sensor)
# Ergebnis = Temp(Sensor)
# if 'Fehler' in str(Ergebnis) :
#     print (Ergebnis)
# else :
#     print ('ausgelesener Sensor' , Sensor , Ergebnis , 'Grad')
# 
# print (80 *'-')
# Sensor = ('hugo')   # ungültiger Sensor
# print ('Test mit Sensor ',Sensor)
# Ergebnis = Temp(Sensor)
# if 'Fehler' in str(Ergebnis) :
#     print (Ergebnis)
# else :
#     print ('ausgelesener Sensor' , Sensor , Ergebnis , 'Grad')
# 
# print (80 *'-')
# Sensor = ('NONE')   # Sensor im Dictionary aber nicht im Systembus
# print ('Test mit Sensor ',Sensor)
# Ergebnis = Temp(Sensor)
# if 'Fehler' in str(Ergebnis) :
#     print (Ergebnis)
# else :
#     print ('ausgelesener Sensor' , Sensor , Ergebnis , 'Grad')
###################################################################

