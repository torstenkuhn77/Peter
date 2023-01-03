# shell : python3 /home/pi/skripts/ColoramaTermcolor.py
# diese Farbsteuerung funktioniert nur bei Ausführung aus der Konsole !
# Beschreibung : https://pypi.org/project/termcolor/

#!/usr/bin/python3
# -*- coding: utf_8 -*-

from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

izahl = 5

# then use Termcolor for all colored text output
print(colored('Hello, World!', 'green', 'on_red'))

print(colored('Hello, World!', 'green'))

print(colored('Hello, World!', 'blue'))

print(colored('Hello, World!', 'yellow', 'on_white'))