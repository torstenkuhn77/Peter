#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Relais import Relais
from RelaisList import RelaisList

#Relais wrapped from GVS

# RelaisList implements iterator protocol, easy to enumerate 

relaisList = RelaisList()

for r in relaisList:
    print(r.name)
    print(r.function)
    print()

relais = relaisList.findRelais("WK4")

if not relais is None:
    relais.Set(False, True, True)

relaisList.ResetAll(False, True, True)

print('ready')
