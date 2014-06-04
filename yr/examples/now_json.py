#!/usr/bin/env python3

from yr.libyr import Yr

weather = Yr('Norge/Telemark/Skien/Skien')
now = weather.now(as_json=True)

print(now)
