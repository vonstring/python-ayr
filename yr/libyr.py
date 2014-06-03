#!/usr/bin/env python3
import sys
import json
import xmltodict # <~ the only external dependency
from yr.utils import Connect, Location, Language, YrException

class Yr:

    def xmlsource(self):
        return self.connect.read()

    def xmltodict(self, xml=None):
        if xml is None:
            xml = self.xmlsource()
        return xmltodict.parse(xml)

    def dicttoxml(self, dictionary):
        return xmltodict.unparse(dictionary, pretty=True)

    def xmltojson(self, xml=None):
        if xml is None:
            xml = self.xmlsource()
        return json.dumps(self.xmltodict(xml), indent=4)

    def now(self, as_json=False): # default is return result as dictionary ;)
        xml = self.dicttoxml({'time': self.xmltodict()['weatherdata']['forecast']['tabular']['time'][0]})
        if as_json:
            return self.xmltojson(xml)
        else:
            return self.xmltodict(xml)

    def __init__(self, location_name, language_name='en'):
        self.location_name = location_name
        self.language_name = language_name
        self.language = Language(self.language_name)
        self.location = Location(self.location_name, self.language)
        self.connect = Connect(self.location)
        self.yr_credit = {
            'text': self.language.dictionary['credit'],
            'url': 'http://www.yr.no/'
        }

if __name__ == '__main__':
    print(Yr('Czech_Republic/Prague/Prague').now(as_json=True))
