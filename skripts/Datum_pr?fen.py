# Test : Routine zur Prüfung , ob es sich um ein gültiges Datum handelt

import time
import datetime

try :
    year  = 2020
#     year  = 'hugo'
    month = 12 # --> gültig
#     month = 13 # --> ungültig
    day   = 12 # --> gültig
#     day   = 32 # --> ungültig
    datum = datetime.date(year,month,day) #Heiligabend
    print ('gültiges Datum : ',datum)
except ValueError: # numerische aber ungültige Werte
    print (year,month,day,' ungültiges Datum')
except TypeError:  # nicht numerische , ungültige Werte
    print (year,month,day,' Datum nicht numerisch')

# Wird ein ungültiges Datum übergeben wird ein ValueError erzeugt, z.b.
# 
# Traceback (most recent call last):
#   File "<pyshell#12>", line 1, in -toplevel-
#     d=datetime.date(2003,12,36)
# ValueError: day is out of range for month