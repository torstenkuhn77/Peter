# Test des dictionary "IORLdict"
# GPIO 21 --> Relais WK4 , 20 --> WK3 , 16 --> WK2 , 12 --> WK1
#####################################################################

IORLdict = {
          "WK1"   : 12,
          "WK1Bez": 'Bezeichnung WK1',"hugo"
          "WK2"   : 16,
          "WK3"   : 20,
          "WK4"   : 21
            }
print ('Inhalt gesamtes dictionary :')
print(IORLdict)
print()

print ('Inhalt Werte zu den Indizes :')
print (IORLdict.get("WK1"))
print (IORLdict.get("WK1Bez"))
print (IORLdict.get("WK2"))
print (IORLdict.get("WK3"))
print (IORLdict.get("WK4"))
print()

WKgesucht = "WK4"
if WKgesucht in IORLdict.keys() : print (WKgesucht , IORLdict.get(WKgesucht),' gefunden im Dictionary ')
else                            : print (WKgesucht ,                         ' nicht gefunden im Dictionary')
print()
WKgesucht = "WK1"+"Bez"
if WKgesucht in IORLdict.keys() : print (WKgesucht , IORLdict.get(WKgesucht),' gefunden im Dictionary ')
else                            : print (WKgesucht ,                         ' nicht gefunden im Dictionary')
print()

WKgesucht = "WK5"
if WKgesucht in IORLdict.keys() : print (WKgesucht , IORLdict.get(WKgesucht),' gefunden im Dictionary ')
else                            : print (WKgesucht ,                         ' nicht gefunden im Dictionary')
print()
NRgesucht = 20
if NRgesucht in IORLdict.values() : print ('Nummer ', NRgesucht , ' gefunden im Dictionary')
else                              : print ('Nummer ', NRgesucht , ' nicht gefunden im Dictionary')
print()
NRgesucht = 11
if NRgesucht in IORLdict.values() : print ('Nummer ', NRgesucht , ' gefunden im Dictionary')
else                              : print ('Nummer ', NRgesucht , ' nicht gefunden im Dictionary')
print()

# in Dictionary schreiben :
IORLdict['WK4'] = 55; # update existing entry
# IORLdict.WK4 = 55
print ('WK4   Wert nach update : ',IORLdict.get("WK4"))
print()

# neuen Eintrag anlegen :
IORLdict['WK5'] = 99  # Add new entry
print (IORLdict.get("WK5"))
print()
# oder
IORLdict['WK6'] = not True  # Add new entry
print (IORLdict.get("WK6"))
print()
