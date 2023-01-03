# Testprogramm Dateioperationen

# Datei zum Lesen öffnen
datei = open('textdatei.txt','r')
print ('----------- Datei geöffnet -----------------')

# Was liefert die Funktion open zurück ? 

print ('jetzt Der open-Befehl liefert :')
print(datei)
print ()

# Welchen Inhalt hat die Datei ? (alle Stellen in allen Zeilen auslesen)

print ('jetzt Dateiinhalt alle Stellen in allen Zeilen :')
print(datei.read())
print ()

# Welchen Inhalt hat die Datei ? (bis zur Stelle i auslesen)
datei = open('textdatei.txt','r')
i = 50
print ('jetzt Dateiinhalt bis zur Stelle i =',i,':')
print(datei.read(i))
print ()

# Welchen Inhalt hat die Datei ? (erste Zeile auslesen)
datei = open('textdatei.txt','r')
print ('jetzt Dateiinhalt erste Zeile :')
print(datei.readline())
print ()

# Welchen Inhalt hat die Datei ? (jede Zeile einzeln auslesen)
datei = open('textdatei.txt','r')
print ('jetzt Dateiinhalt jede Zeile einzeln :')
for zeile in datei:
    print("nächste Zeile: ")
    print(zeile)
print ()


# Datei gelesen und schließen
datei.close()
print ('----------- Datei geschlossen -----------------')

