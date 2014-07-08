#!/usr/bin/env python3

from yr.libyr import Yr

#weather = Yr(location_name="Italy/Trentino_and_South-Tirol/San_Michele_all'Adige")
weather = Yr(location_xyz=(11.13358, 46.19291, 210)) # xyz for Italy/Trentino_and_South-Tirol/San_Michele_all'Adige

all_parameters = [ # from the api is possible to obtain more info
    'humidity',
    'cloudiness',
    'lowClouds',
    'mediumClouds',
    'highClouds',
    'dewpointTemperature',
    'precipitation',
    'windDirection',
    'windSpeed',
    'temperature',
    'pressure',
]

weather.py2csv(parameters=all_parameters) # print to stdout all values
print()
weather.py2csv(daily=True, parameters=all_parameters) # print to stdout daily values
