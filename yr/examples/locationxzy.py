#!/usr/bin/env python3

from yr.libyr import Yr

#location for Italy/Trentino_and_South-Tirol/San_Michele_all'Adige

san_michele = (46.19291, 11.13358, 210)
weather = Yr(xyz=san_michele)

for forecast in weather.forecast(as_json=True):
    print(forecast)
