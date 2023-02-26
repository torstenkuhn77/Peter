#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Relais import Relais
from Relais import RelaisList

#Relais wrapped from GVS

# RelaisList implements iterator protocol, easy to enumerate 
for r in RelaisList():
    print(r.Name)
    print(r.Function)
    print()

print('ready')
