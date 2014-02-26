#!/usr/bin/env python3

import os.path, sys
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_directory)
from libyr import Yr

#weather = Yr('Norge/Telemark/Skien/Skien')
weather = Yr('Czech_Republic/Prague/Prague')

print(weather.now(as_json=True))
