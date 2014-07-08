#!/usr/bin/env python3

import sys
import json
import xmltodict # <~ the only external dependency
from yr.utils import Connect, Location, LocationXYZ, Language, YrException, YrCSV

class Yr:

    def py2json(self, python):
        return json.dumps(python, indent=4)

    def xml2dict(self, xml):
        return xmltodict.parse(xml)

    def dict2xml(self, dictionary):
        return xmltodict.unparse(dictionary, pretty=True)

    def py2csv(self, outputfile, daily=False, stats=['min', 'max', 'avg'],
               interval=[0, 6], parameters=['precipitation', 'windDirection',
                                            'windSpeed', 'temperature',
                                            'pressure']):
        """Return CSV file of forecast data

        :param str outputfile: the complete path and name to output csv file
        :param bool daily: by default (False) it write all forecast records,
                           True to write one record for each day
        :param list stats: a list with statistical value to calculate, admited
                           values are: 'min', 'max', 'avg'.
                           Used only with daily=True
        :param list interval: list of forecast interval to use, 0 has be set
                              everytime as first element, other options are:
                              3 for the three hours precipitation forecast,
                              6 for the six hours precipitation forecast
        :param list parameters: list of parameters to save in the CSV file.....
        """
        data = self.forecast()
        yrcsv = YrCSV(data, parameters, stats, interval)
        if daily:
            yrcsv.write_daily(outputfile)
        else:
            yrcsv.write_all(outputfile)

    def py2result(self, python, as_json=False): # default is return result as dictionary ;)
        if as_json:
            return self.py2json(python)
        else:
            return python

    def forecast(self, as_json=False):
        if self.location_xyz:
            times = self.dictionary['weatherdata']['product']['time']
        else:
            times = self.dictionary['weatherdata']['forecast']['tabular']['time']
        for time in times:
            yield self.py2result(time, as_json)

    def now(self, as_json=False):
        return next(self.forecast(as_json))

    def __init__(self, location_name=None, location_xyz=None, forecast_link='forecast', language_name='en'):
        self.language_name = language_name
        self.forecast_link = forecast_link       
        self.language = Language(self.language_name)
        if location_name:
            self.location_name = location_name
            self.location_xyz = None
            self.location = Location(self.location_name, self.forecast_link, self.language)
        elif location_xyz:
            self.location_name = None
            self.location_xyz = location_xyz
            self.location = LocationXYZ(location_xyz[0], location_xyz[1], location_xyz[2])
        else:
            raise YrException("location_name or location_xyz parameter must be set")
        self.connect = Connect(self.location)
        self.xml_source = self.connect.read()
        self.dictionary = self.xml2dict(self.xml_source)
        self.credit = {
            'text': self.language.dictionary['credit'],
            'url': 'http://www.yr.no/'
        }

if __name__ == '__main__':
    print(Yr(location_name='Czech_Republic/Prague/Prague').now(as_json=True))
