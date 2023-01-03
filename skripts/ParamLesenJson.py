# skript zum Einlesen von Werten aus einer JSON Datei
# shell : python3 /home/pi/skripts/vonTo/ReadConfigJson.py

import json

# JSON Datei einlesen
with open('/home/pi/skripts/Parameter.json') as f:
    config_raw = f.read()
# Konvertieren der gelesenen bytes in einen JSON string
config = json.loads(config_raw)

# testweise dump ausgeben
print ('dump json-Datei   :')
print(json.dumps(config, indent = 4))

print ()
print ('eingelesene Werte :')

if config['Parameter']['Raumheizung'] != 'ein' and config['Parameter']['Warmwasser'] != 'ein' :
    raise AssertionError('Verarbeitung nicht möglich , keiner der Parameter Raumheizung oder Warmwasser auf "ein" gesetzt !')

# auf die einzelenen werte kann man jetzt wie folgt zugreifen
print ('Raumheizung ',config['Parameter']['Raumheizung'],' Warmwasser ',config['Parameter']['Warmwasser'])

DTvon = config['Parameter']['Tagsteuerung']['DTvon']
DTbis = config['Parameter']['Tagsteuerung']['DTbis']
print('Tagsteuerung     von',DTvon,'bis',DTbis,)

#NAvon = config['Parameter']['Nachtaufladung']['NAvon']
#NAbis = config['Parameter']['Nachtaufladung']['NAbis']
#print('Nachtaufladung   von',NAvon,'bis',NAbis)

BZvon = config['Parameter']['boostZeit']['von']
BZbis = config['Parameter']['boostZeit']['bis']
print('Boost Zeit       von',BZvon,'bis',BZbis)

RTmin = config['Parameter']['Raumtemperatur']['RTmin']
RTmax = config['Parameter']['Raumtemperatur']['RTmax']
print('Raumtemperatur   min',RTmin,'max',RTmax)

BTmin = config['Parameter']['Boilertemperatur']['BTmin']
BTmax = config['Parameter']['Boilertemperatur']['BTmax']
print('Boilertemperatur min',BTmin,'max',BTmax)

VTmax = config['Parameter']['Vorlauftemperatur']['VTmax']
print('Vorlauftemperatur         max',VTmax)

KTmin = config['Parameter']['Kesseltemperatur']['KTmin']
KTmax = config['Parameter']['Kesseltemperatur']['KTmax']
KTboost = config['Parameter']['Kesseltemperatur']['KTboost']
print('Kesseltemperatur min',KTmin,'max',KTmax,'boost ab',KTboost)

wait = config['Parameter']['Zyklus']['Sekunden']
print('Programmzyklus  ',wait,'Sekunden')
Nachtfaktor = config['Parameter']['Zyklus']['NachtFak']
print('Nachtfaktor     ',Nachtfaktor)