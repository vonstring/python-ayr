#!/usr/bin/env python3

from yr.libyr import Yr

#location for Italy/Trentino_and_South-Tirol/San_Michele_all'Adige

san_michele = (11.13358, 46.19291, 210)
weather = Yr(xyz=san_michele)

#from the api is possible to obtain more info
all_parameters = ['humidity', 'cloudiness', 'lowClouds', 'mediumClouds',
                  'highClouds', 'dewpointTemperature', 'precipitation',
                  'windDirection', 'windSpeed', 'temperature', 'pressure']

#print to stdout all values
weather.py2csv(None, parameters=all_parameters)

print("\n")
#print to stdout daily values
weather.py2csv(None, True, parameters=all_parameters)
