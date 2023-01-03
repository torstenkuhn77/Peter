# script name : /home/pi/skripts/prod/Func_Sensor-klein.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-


# shell befehl : cat /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
# Ergebnis :
# pi@PB-raspberrypi:~ $ cat /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
# 92 02 55 05 7f a5 a5 66 75 : crc=75 YES
# 92 02 55 05 7f a5 a5 66 75 t=41125
# pi@PB-raspberrypi:~ $ 


sensorKT = '/sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave'
f = open(sensorKT, 'r')
line = f.readline()
line1 = f.readline()
f.close()
temperaturStr = line1.find('t=')
# für Testzwecke :
print ('Sensor :',sensorKT)
print ('line :',line)
print ('line1 :',line1)
print ('temperaturStr :',temperaturStr)
print ()
# Ergebnis :
# /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
# 95 02 55 05 7f a5 a5 66 a5 : crc=a5 YES
# 
# -1
