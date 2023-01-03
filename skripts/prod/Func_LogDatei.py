# shell :  python3 /home/pi/skripts/Func_LogDatei.py
#          python3 /home/pi/skripts/Func_LogDatei.py.Schreiben

#!/usr/bin/python3
# -*- coding: utf-8 -*-

def Schreiben (time_stamp , LogText , my_dir , my_file) :
    
    from pathlib import Path
           
    file_name = my_dir + '/' + my_file
    
    try:    # Prüfen , ob Verzeichnis und Datei existieren
        datei = open(file_name, 'r')
        
    except IOError :
        LogText = 'Fehler : cannot open ' + file_name
        test_dir = Path(my_dir)    
        if not test_dir.is_dir():
            LogText = LogText + ' kein Log-Satz , Verzeichnis ' + my_dir + ' existiert nicht'
        else :
            test_file = Path(file_name)
            if not test_file.is_file():
                LogText = LogText + ' kein Log-Satz , Datei ' + my_file + ' existiert nicht'            

    else :
        # vorhandene Datei öffnen , Tageswechsel Inhalt mit a , \n in neuer Zeile anhängen
        Wechseltext = ''
        datei = open(file_name,'r')                # Log-Datei öffnen
        last_line = datei.readlines()[-1]          # letzte Zeile lesen
        if time_stamp[0:10] != last_line[0:10] :   # Wechsel des Tages --> neue Zeile
            Wechseltext = (time_stamp + ' ............ neuer Tag .........................................')
        datei.close()
        # vorhandene Datei öffnen , Inhalt mit a , \n in neuer Zeile anhängen
        datei = open(file_name,'a')
        if Wechseltext != '' :
            datei.write('\n' + Wechseltext)
        LogText = time_stamp + ' ' + LogText
        datei.write('\n' + LogText)
        datei.close()
        LogText = time_stamp + ' Log-Satz geschrieben in Datei ' + file_name
            
    return (LogText)

#####################################
# Beispiel : letzte Zeile lesen
#f_read = open("filename.txt", "r")
#last_line = f_read.readlines()[-1]
#f_read.close()
#####################################

