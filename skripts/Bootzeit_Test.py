# Testprogramm f.d. Boost-Zeit

DTvon = '08:59'

# Beginn boost erst 1 Stunde nach Beginn der Tagsteuerung
i1 = DTvon [0]
i2 = DTvon [1]
i3bis5 = DTvon [2] + DTvon [3] + DTvon [4]

i2 = int (i2) + 1
i2 = str (i2)
boostfrom = i1 + i2 + i3bis5
# 1 Stelle nach links schieben , wenn hh 2-stellig
if boostfrom [0] == '0' and len(boostfrom) >= 6 :
    boostfrom = boostfrom[1] + boostfrom[2] + boostfrom[3] + boostfrom[4] + boostfrom[5]
if boostfrom > '22:59' :
    print ('Fehler bei Angabe der Tagzeit',DTvon,'--> boost Zeit ',boostfrom)


print (boostfrom)




