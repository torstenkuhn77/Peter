# Kesseltemperatur  Sensor 28-030997790a01
# oben

# Vorlauftemperatur Sensor 28-030997790e32

# Raumtemperatur    Sensor 28-01186c88d8ff geändert seit 25.12,2020

# Boilertemperatur  Sensor 28-0316a27937aa

# Wohnen            Sensor 28-01186c88d8ff  (hinzugekommen 23.12.2020 neu fürs Wohnzimmer)

# Kesseltemperatur  Sensor 28-0309977914a4 seit 29.01,2021
# unten

# shell Befehle zum Auslesen :

# allle Sensoren auslesen :
# cd /sys/bus/w1/devices
# ls
# Ergebnis :
# pi@PB-raspberrypi:~ $ cd /sys/bus/w1/devices
# pi@PB-raspberrypi:/sys/bus/w1/devices $ ls
# 28-01186c88d8ff  28-030997790a01  28-030997790e32  28-0309977914a4  28-0316a27937aa  w1_bus_master1
# pi@PB-raspberrypi:/sys/bus/w1/devices $ 

# einen Sensor auslesen :
# cat /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
# Ergebnis :
# pi@PB-raspberrypi:~ $ cat /sys/bus/w1/devices/w1_bus_master1/28-030997790a01/w1_slave
#9c 04 55 05 7f a5 a5 66 42 : crc=42 YES
#9c 04 55 05 7f a5 a5 66 42 t=73750
#pi@PB-raspberrypi:~ $ 
