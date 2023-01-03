# shell : python3 /home/pi/skripts/Relais_EIN-AUS.py
# die Farbsteuerung funktioniert nur bei Ausführung aus der Konsole !
# Beschreibung : https://pypi.org/project/colorama/

# -*- coding: utf-8 -*-

# Programm zum turnusmäßigen Einschalten des Relais mit GPIO Nummer xx

import time , sys , RPi.GPIO as GPIO

from colorama import init, Fore, Style
          # init(autoreset=True), wenn Farbe nur je Printstatement gelten soll
init()    # init()Farbe gilt bis Programmende


print(Fore.GREEN + Style.BRIGHT + time.strftime("%d.%m.%Y %H:%M:%S") , 'Start Relais EIN-AUS , Beenden mit CTRL+C ')


GPIO.setmode(GPIO.BCM) #  GPIO statt Board Nummern

# GPIO 21 --> Relais K4 , 20 --> K3 , 16 --> K2 , 12 --> K1
RELAIS = 'REC'
RELAIS_GPIO = 18

GPIO.setwarnings(False)
GPIO.setup(RELAIS_GPIO, GPIO.OUT) # GPIO Modus zuweisen
GPIO.setwarnings(True)


# Anzahl Schaltvorgänge festlegen , Initialisieren , Anzahlvorgänge = float("inf") --> unendlich viele
Anzahlvorgänge = float(2)
Aktvorgang = int(1)

try:
    while Aktvorgang <= Anzahlvorgänge :
        

        if Aktvorgang == 1 : time.sleep(0) # kein Warten beim 1. Vorgang
        else :               time.sleep(1) # Nach x Sekunden nächster Vorgang
        
        
                
        GPIO.output(RELAIS_GPIO, GPIO.LOW)  # Relais einschalten
                
        time.sleep(1)                       # x Sekunden warten
                
        GPIO.output(RELAIS_GPIO, GPIO.HIGH) # Relais ausschalten
        
        print(Fore.CYAN + Style.NORMAL + time.strftime("%d.%m.%Y %H:%M:%S"),Aktvorgang,'Relais',RELAIS ,'GPIO',RELAIS_GPIO,'EIN / AUS ')

        Aktvorgang = Aktvorgang + 1         # Anzahlvorgänge hochzählen    

        if Aktvorgang == Anzahlvorgänge : time.sleep(1) # beim letzten Vorgang nur y Sek warten
        else :                            time.sleep(3) # bei jedem Vorgang y Sek warten
        
except KeyboardInterrupt:
    # Programm wird beendet wenn CTRL+C gedrückt wird.
    GPIO.cleanup()
    print(Fore.GREEN + Style.BRIGHT + time.strftime("%d.%m.%Y %H:%M:%S") , 'KeyboardInterrupt durch CTRL+C')

except Exception as e:
    print(Fore.RED   + Style.BRIGHT + time.strftime("%d.%m.%Y %H:%M:%S") , 'Exception' , str(e))
    sys.exit(1)

finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    print(Fore.GREEN + Style.BRIGHT + time.strftime("%d.%m.%Y %H:%M:%S") , 'Stop  Relais EIN-AUS')
    GPIO.cleanup()
    sys.exit(0)
