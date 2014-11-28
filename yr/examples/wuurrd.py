#!/usr/bin/env python3

from yr.libyr import Yr

weather = Yr(location_name=u'Norge/Telemark/Skien/Skien')

wind_speed = dict()
wind_speed[u'data'] = [{u'from': forecast[u'@from'], u'to': forecast[u'@to'], u'speed': float(forecast[u'windSpeed'][u'@mps'])} for forecast in weather.forecast()]
wind_speed[u'credit'] = weather.credit

print wind_speed
