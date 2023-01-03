# shell :  python3 /home/pi/skripts/prod/Log_Relais_Ini.py
# Programm zum Initialisieren / reset der Text-Datei Log_Relais.txt

#!/usr/bin/python

from pathlib import Path

import time , GVS

my_dir  = GVS.RelLogDir
my_file = GVS.RelLogFile

## für Testzwecke :
#my_dir   = 'test'    # für Test Verzeichnis existiert nicht
#my_file = 'test.txt' # für Test Verzeichnis existiert nicht

file_name  =  my_dir +'/' + my_file
time_stamp = time.strftime("%Y.%m.%d %H:%M:%S")

try:    # Prüfen , ob Verzeichnis und Datei existieren
    
    datei = open(file_name, 'r') # öffnen zum lesen
    print ()
    
except IOError as e :
    print ('IOError' , str(e))
    my_dir = Path(my_dir)    
    if not my_dir.is_dir():
        print (time_stamp,' Verzeichnis existiert nicht')
    else :
        my_file = Path(file_name)
        if not my_file.is_file():
            print (time_stamp,' Datei existiert nicht')
    print ()
    
else:   # Verarbeitung nur wenn Verzeichnis und Datei existieren
    # vorhandene Datei öffnen , Inhalt löschen und überschreiben
    datei = open(file_name,'w') # öffnen zum schreiben
    Text = time_stamp + '  Logdatei für Schaltvorgänge der Relais initialisiert'
    datei.write(Text)
    # vorhandene Datei öffnen , Inhalt in neuer Zeile anhängen
    datei = open(file_name,'a') # öffnen zum anhängen
    Text = '\n' + time_stamp + ' ' + 83 * '-'
    datei.write(Text)
    # vorhandene Datei öffnen , Inhalt ausgeben
    datei = open(file_name,'r') # öffnen zum lesen
    print (time_stamp,' Datei ',file_name  ,' initialisiert')
    print ()
    print ('Dateiinhalt nach Initialisierung , zeilenweise : ')
    print ()
    print(datei.read())
    #print(datei.readlines())
    print ()
    datei.close()
        

