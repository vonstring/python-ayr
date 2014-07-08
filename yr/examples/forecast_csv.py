#!/usr/bin/env python3

from yr.libyr import Yr

#location for Italy/Trentino_and_South-Tirol/San_Michele_all'Adige

weather = Yr(location_name="Italy/Trentino_and_South-Tirol/San_Michele_all'Adige")

#print to stdout all values
weather.py2csv(None)

print("\n")
#print to stdout daily values
weather.py2csv(None, True)
