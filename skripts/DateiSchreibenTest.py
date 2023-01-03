# shell :  python3 /home/pi/skripts/DateiSchreibenTest.py
# Test Programm zum Lesen und Schreiben in eine Datei

#!/usr/bin/python

from pathlib import Path

import Func_LogDatei , time , GVS

my_dir  = '/home/pi/skripts'
#my_dir   = 'test' # für Test Verzeichnis existiert nicht
my_file = 'textdatei_1.txt'
#my_file = 'test.txt' # für Test Verzeichnis existiert nicht
file_name =  my_dir +'/' + my_file

try:    # Prüfen , ob Verzeichnis und Datei existieren
    datei = open(file_name, 'r')

except OSError :
    print ('cannot open', file_name)
    my_dir = Path(my_dir)    
    if not my_dir.is_dir():
        print ('Verzeichnis existiert nicht')
    else :
        my_file = Path(file_name)
        if not my_file.is_file():
            print ('Datei existiert nicht')
            
else:   # Verarbeitung , wenn Verzeichnis und Datei existieren

    # vorhandene Datei öffnen , Inhalt ausgeben
    datei = open(file_name,'r')
    print ('Dateiinhalt vor Bearbeitung : ')
    print(datei.read())
    print ()

    # vorhandene Datei öffnen , Inhalt anhängen
    datei = open(file_name,'a')
    Text = ' + Anhang ...'
    datei.write(Text)
    datei = open(file_name,'r')
    print ('Dateiinhalt nach Bearbeitung mit a = append : ')
    print(datei.read())
    print ()

    # vorhandene Datei öffnen , Inhalt in neuer Zeile anhängen
    datei = open(file_name,'a')
    Text = '\n' + ' + neue Zeile ...'
    datei.write(Text)
    datei = open(file_name,'r')
    print ('Dateiinhalt nach Bearbeitung mit a,n = neue Zeile anhängen : ')
    print(datei.read())
    print ()

    # vorhandene Datei öffnen , Inhalt löschen und überschreiben
    datei = open(file_name,'w')
    Text = 'Dateiinhalt gelöscht und initialisiert'
    datei.write(Text)
    datei = open(file_name,'r')
    print ('Dateiinhalt nach Bearbeitung mit w = Inhalt gelöscht : ')
    print(datei.read())
    print ()

    datei.close()
        

#Test der Funktion Func_LogDatei 

print ()
print ('Test der Funktion Func_LogDatei :')
print ()
LogText = 'Versuch mit falschem directory'
my_dir   = 'hugo' 
my_file = 'textdatei_1.txt'
LogText = Func_LogDatei.Schreiben (time.strftime("%Y.%m.%d %H:%M:%S") , LogText , my_dir , my_file)
if LogText[0:5] == 'Fehler' : # Fehler beim Schreiben der Logdatei
    LogText = Fore.RED + Style.BRIGHT + LogText
print (LogText)
print ()

LogText = 'Versuch mit falschem file'
my_dir  = '/home/pi/skripts' 
my_file = 'werner.txt'
LogText = Func_LogDatei.Schreiben (time.strftime("%Y.%m.%d %H:%M:%S") , LogText , my_dir , my_file)
if LogText[0:5] == 'Fehler' : # Fehler beim Schreiben der Logdatei
    LogText = Fore.RED + Style.BRIGHT + LogText
print (LogText)
print ()

LogText = 'Versuch mit korrekter Pfadangabe'
my_dir  = '/home/pi/skripts'
my_file = 'textdatei_1.txt'
LogText = Func_LogDatei.Schreiben (time.strftime("%Y.%m.%d %H:%M:%S") , LogText , my_dir , my_file)
if LogText[0:5] == 'Fehler' : # Fehler beim Schreiben der Logdatei
    LogText = Fore.RED + Style.BRIGHT + LogText
print (LogText)
print ()