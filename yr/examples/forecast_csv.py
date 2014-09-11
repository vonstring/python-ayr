#!/usr/bin/env python3

from yr.libyr import Yr

weather = Yr(location_name="Italy/Trentino_and_South-Tirol/San_Michele_all'Adige")
#weather = Yr(location_xyz=(11.13358, 46.19291, 210)) # xyz for Italy/Trentino_and_South-Tirol/San_Michele_all'Adige

l = weather.py2list() # print to stdout all values
print(l)
print()
l = weather.py2list(daily=True) # print to stdout daily values
print(l)
