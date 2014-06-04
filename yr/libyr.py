#!/usr/bin/env python3

import sys
import json
import xmltodict # <~ the only external dependency
from yr.utils import Connect, Location, Language, YrException

class Yr:

    def dict2json(self, dictionary):
        return json.dumps(dictionary, indent=4)

    def xml2dict(self, xml):
        return xmltodict.parse(xml)

    def dict2xml(self, dictionary):
        return xmltodict.unparse(dictionary, pretty=True)

    def dict2result(self, dictionary, as_json=False): # default is return result as dictionary ;)
        if as_json:
            return self.dict2json(dictionary)
        else:
            return dictionary

    def forecast(self, as_json):
        times = self.dictionary['weatherdata']['forecast']['tabular']['time']
        for time in times:
            yield self.dict2result({'time': time}, as_json)

    def now(self, as_json):
        return next(self.forecast(as_json))

    def __init__(self, location_name, language_name='en'):
        self.location_name = location_name
        self.language_name = language_name
        self.language = Language(self.language_name)
        self.location = Location(self.location_name, self.language)
        self.connect = Connect(self.location)
        self.xml_source = self.connect.read()
        self.dictionary = self.xml2dict(self.xml_source)
        self.credit = {
            'text': self.language.dictionary['credit'],
            'url': 'http://www.yr.no/'
        }

if __name__ == '__main__':
    print(Yr('Czech_Republic/Prague/Prague').now(as_json=True))
