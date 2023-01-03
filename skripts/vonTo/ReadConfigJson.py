# shell : python3 /home/pi/skripts/vonTo/ReadConfigJson.py

import json

# with open('.\SteuerungConfig.json') as f:
with open('/home/pi/skripts/vonTo/SteuerungConfig.json') as f:
    config_raw = f.read()

# konvertiert die gelesenen bytes in einen json string
config = json.loads(config_raw)
# pretty print
print(json.dumps(config, indent = 4))

# auf die einzelenen werte kann man jetzt wie folgt zugreifen
DTvon = config['Konfiguration']['Tagsteuerung']['DTvon']
print(DTvon)
