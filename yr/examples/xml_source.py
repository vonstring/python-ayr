#!/usr/bin/env python3

from yr.libyr import Yr

weather = Yr('Norge/Telemark/Skien/Skien')

print(weather.xml_source)
