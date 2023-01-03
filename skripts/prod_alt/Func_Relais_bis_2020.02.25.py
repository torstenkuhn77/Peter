# shell : python3 /home/pi/skripts/Func_Relais.py

# die Farbsteuerung funktioniert nur bei Ausführung aus der Konsole !
# Beschreibung : https://pypi.org/project/colorama/

# Programm zum Ein-/Ausschalten des Relais abc mit GPIO Nummer xy

# -*- coding: utf-8 -*-

import time , RPi.GPIO as GPIO

from colorama import init , Fore , Back , Style
                    # init(autoreset=True) Farbe gilt nur je Printposition
                    # init()               Farbe gilt bis Programmende
                    #Farben :
                    #Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                    #Style: DIM, NORMAL, BRIGHT, RESET_ALL

init(autoreset=True)

GPIO.setmode(GPIO.BCM) #  GPIO statt Board Nummern

# GPIO 21 --> Relais WK4 , 20 --> WK3 , 16 --> WK2 , 12 --> WK1
##############################################################################################

def Schaltung (RELAIS , RELAIS_GPIO , Funktion , Schalter) :

    GPIO.setwarnings(False)
    GPIO.setup(RELAIS_GPIO,GPIO.OUT)   # GPIO Modus zuweisen , warning abschalten
    GPIO.setwarnings(True)
    
    Text = Fore.RED + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + Funktion
    
    RELAISliste = ["WK1","WK2","WK3","WK4"]   # prüfen ob Relais definiert
    if RELAIS not in RELAISliste :
        Text =  Text + " Fehler Relais " + RELAIS + ' nicht zulässig'
 
    GPIOliste = [12,16,20,21]                  # prüfen ob GPIO verdrahtet
    if RELAIS_GPIO not in GPIOliste :
        Text = Text + " Fehler GPIO " + str(RELAIS_GPIO) + ' nicht zulässig'

    Schalterliste = ["ein","aus"]              # prüfen ob Schalter korrekt
    if Schalter not in Schalterliste :
        Text = Text + " Fehler Schalter " + Schalter + ' nicht zulässig'
                                                     # Schaltvorgang ausführen
    
    # keine Fehler festgestellt -->   Schaltvorgang ausführen
    if Text == Fore.RED + Style.BRIGHT + time.strftime("%Y.%m.%d %H:%M:%S") + Funktion :
        
        Text = time.strftime("%Y.%m.%d %H:%M:%S") + Funktion + ' '
        
        if Schalter == 'ein':
            GPIO.output(RELAIS_GPIO, GPIO.LOW)      # Relais einschalten
            Text = Text + Fore.BLACK + Back.YELLOW
            Text = Text + 'Relais ' + RELAIS + ' GPIO ' + str(RELAIS_GPIO) + ' ein' 

        if Schalter == 'aus':
            GPIO.output(RELAIS_GPIO, GPIO.HIGH)     # Relais ausschalten
            Text = Text + Fore.BLACK + Back.YELLOW
            Text = Text + 'Relais ' + RELAIS + ' GPIO ' + str(RELAIS_GPIO) + ' aus'
            
    return (Text)