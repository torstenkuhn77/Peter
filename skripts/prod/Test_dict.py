import numpy as np

import GVS
# # in GVS : 
# SensTyp  = ['DS18B20','Platzhalter']                    # gültige Sensoren - Typen
# SensList = ['Raum','Kessel','Vorlauf','Boiler']         # gültige Temperatur-Sensoren vom Typ DS18B20

def Sens (Typ) :  # Liste aller Sensoren vom Typ 'yxz' mit Ausnahme derer , die mit 'void' gekennzeichnet sind
    SEN_Liste = []
    print('es wurden folgende Sensoren vom Typ' , Typ , 'in GVS.SensTab gefunden :')
    for key, value in GVS.SensTab.items():
        if not '_' in key :
            if GVS.void_key not in key :
                SEN_Liste.append (key) ;
            print (key ,10*' ' , 'Typ' ,GVS.SensTab.get(key + '_Typ') )
#     print('es wurde folgende Sensoren-Liste zum Typ ' , Typ , ' erzeugt (SEN_Liste) :')        
#     print('(welche Sensoren vom Typ ' , Typ , '  gibt es ?') 
#     print(SEN_Liste)
#     print ('Länge Sensoren-Liste (SEN_Liste)    : ' , len (SEN_Liste))
    return (SEN_Liste)

# GVS.SEN_Typ_Liste aufbauen aus GVS.SensTab
def SensTyp () :
    SEN_Typ_Liste = []
    for key, value in GVS.SensTab.items():
        if '_Typ' in key :
            if GVS.SensTab.get(key , '_Typ') not in SEN_Typ_Liste and GVS.void_key not in key :
                SEN_Typ_Liste.append (GVS.SensTab.get(key , '_Typ')) ;
#     print('es wurde folgende Typen-Liste erzeugt (SEN_Typ_Liste) :')
#     print('(welche Sensoren-Typen gibt es ?)')
#     print(SEN_Typ_Liste)
#     print ('Länge Sensoren-Typen-Liste (SEN_Typ_Liste) : ' , len (SEN_Typ_Liste))
    return (SEN_Typ_Liste)


print ()
Ergebnis = SensTyp()
print('(welche Sensoren-Typen gibt es in GVS.SensTab ?)')
print ('--> Sensoren-Typ-Liste Länge : ',len(Ergebnis) ,' Inhalt : ',Ergebnis)
print ()

Type = 'DS18B20'
Ergebnis = Sens(Type)
print()
print('(welche Sensoren vom Typ ' , Type , '  gibt es in GVS.SensTab ?')
print ('--> Sensoren-Liste     Länge : ',len(Ergebnis),' Inhalt : ',Ergebnis)

# print()
# TypTab = np.array([])
# print('es wurde folgende Sensoren-Typen-/Sensoren-Tabelle erzeugt (TypTab) :')
# print('(zu welchem Sensoren-Typ gehören welche Sensoren ?)')
# TypTab = np.array(['DS18B20',tuple(SEN_Liste)])
# print(TypTab)


