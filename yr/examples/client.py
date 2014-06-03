#!/usr/bin/env python3

import sys
import os.path
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_directory)
from libyr import Yr

weather = Yr('Norge/Telemark/Skien/Skien')
print(weather.now())
