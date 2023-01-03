# Programm zum turnusmäßigen Ein-/Ausschalten des Relais für TFA3035 mit GPIO Nummer 16 Wohnzimmer WK2

import time , sys , math , RPi.GPIO as GPIO

# GPIO 21 --> Relais K4 , 20 --> K3 , 16 --> K2 , 12 --> K1
RELAIS      = 'WK3'
RELAIS_GPIO = 20

# Anzahl Schaltvorgänge festlegen , Initialisieren , Anzahlvorgänge = int(x) oder math.inf--> unendlich viele
Anzahlvorgänge = math.inf
Aktvorgang     = int(1)
Pause          = 60  # Pause zwischen Vorgängen

print(time.strftime("%d.%m.%Y %H:%M:%S") , 'Start Relais',RELAIS,RELAIS_GPIO,'TFA3035 EIN-AUS , Beenden mit CTRL+C ')

GPIO.setmode(GPIO.BCM) #  GPIO statt Board Nummern

GPIO.setwarnings(False)

GPIO.setup(RELAIS_GPIO, GPIO.OUT) # GPIO Modus zuweisen

GPIO.setwarnings(True)

try:
    while Aktvorgang <= Anzahlvorgänge :
        
        if Aktvorgang == 1 : time.sleep(0)      # kein Warten beim 1. Vorgang
        else :               time.sleep(Pause)  # Nach Pause nächster Vorgang      
                
        Aktvorgang = Aktvorgang + 1             # Anzahlvorgänge hochzählen        
      
        GPIO.output(RELAIS_GPIO, GPIO.LOW)  # Relais einschalten
                
        time.sleep(0.5)                     # x Sekunden warten
                
        GPIO.output(RELAIS_GPIO, GPIO.HIGH) # Relais ausschalten
        
        print(time.strftime("%d.%m.%Y %H:%M:%S") , 'Vorgang',(Aktvorgang - 1) , RELAIS , RELAIS_GPIO , 'EIN-AUS ')
             
        
except KeyboardInterrupt:
    # Programm wird beendet wenn CTRL+C gedrückt wird.
    print(time.strftime("%d.%m.%Y %H:%M:%S") , 'KeyboardInterrupt CTRL+C')

except Exception as e:
    print(time.strftime("%d.%m.%Y %H:%M:%S") , 'Exception' , str(e))
    sys.exit(1)

finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    print(time.strftime("%d.%m.%Y %H:%M:%S") , 'Stop  Relais',RELAIS,RELAIS_GPIO,'TFA3035 EIN-AUS')
    GPIO.cleanup()
    sys.exit(0)

