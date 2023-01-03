# Test einer Listenbearbeitung als Rückgabe aus einer Funktion


def TestFunk (K2_Rel , K2_Schalter) :
    K2_Rel = 'xy3'
    K2_Schalter = False
    l = [K2_Rel , K2_Schalter]
#     K2_Rel = 'ab1'
#     K2_Schalter = True
#     l = [K2_Rel , K2_Schalter]
    return (l)

K2_Rel = 'KK2'
K2_Schalter = True

print (TestFunk(K2_Rel , K2_Schalter))
print ()
String = (TestFunk(K2_Rel , K2_Schalter))
print (String , 'so sieht der zurückgegebene String aus')
print ()
print (String.pop(0),String.pop(0))   # strings von erster Position
String = (TestFunk(K2_Rel , K2_Schalter))
print ()
print (String.pop(0))
print (String.pop(0))
print ()
String = (TestFunk(K2_Rel , K2_Schalter))
print (String.pop(),String.pop())     # strings von letzter Position 
print ()
print (String , 'der String ist also , wenn alle "abgepoppt" sind , leer !')

