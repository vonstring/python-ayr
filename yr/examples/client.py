#!/usr/bin/env python3

from yr.libyr import Yr

weather = Yr('Norge/Telemark/Skien/Skien')

#now_json = weather.now(as_json=True)
#print(now_json)
#
#for forecast in weather.forecast(as_json=True):
#    print(forecast)
#
#print(weather.xml_source)
#print(weather.dictionary)
#print(weather.credit)

wind_speed = dict()
wind_speed['data'] = [{'from': forecast['@from'], 'to': forecast['@to'], 'speed': float(forecast['windSpeed']['@mps'])} for forecast in weather.forecast()]
wind_speed['credit'] = weather.credit

print(wind_speed)
