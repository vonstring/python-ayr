#!/usr/bin/env python3

import logging
import json
import xmltodict  # <~ the only external dependency
from ayr.utils import Connect, Location, API_Locationforecast, Language, YrException
import asyncio

class Yr:

    default_forecast_link = 'forecast'
    default_language_name = 'en'

    def py2json(self, python):
        return json.dumps(python, indent=4)

    def xml2dict(self, xml):
        return xmltodict.parse(xml)

    def dict2xml(self, dictionary):
        return xmltodict.unparse(dictionary, pretty=True)

    def py2result(self, python, as_json=False):  # default is return result as dictionary ;)
        if as_json:
            return self.py2json(python)
        else:
            return python

    async def forecast(self, as_json=False):
        data = await self.data()
        if self.coordinates:
            times = data['weatherdata']['product']['time']
        else:
            times = data['weatherdata']['forecast']['tabular']['time']
        return [self.py2result(time, as_json) for time in times]

    async def now(self, as_json=False):
        forecast = await self.forecast(as_json)
        return forecast[0]

    def __init__(
            self,
            location_name=None,
            coordinates=None,
            location_xyz=None,
            forecast_link=default_forecast_link,
            language_name=default_language_name,
    ):
        self.forecast_link = forecast_link
        self.language_name = language_name
        self.language = Language(language_name=self.language_name)

        if location_xyz:
            if len(location_xyz) > 2:
                coordinates = (location_xyz[1], location_xyz[0], location_xyz[2])
            else:
                coordinates = (location_xyz[1], location_xyz[0])
            self.location_xyz = location_xyz

        if location_name:
            self.location_name = location_name
            self.coordinates = None
            self.location = Location(
                location_name=self.location_name,
                forecast_link=self.forecast_link,
                language=self.language,
            )
        elif coordinates:
            self.location_name = None
            self.coordinates = coordinates
            if len(self.coordinates) > 2:
                self.location = API_Locationforecast(
                    lat=self.coordinates[0],
                    lon=self.coordinates[1],
                    msl=self.coordinates[2],
                    language=self.language,
                )
            else:
                self.location = API_Locationforecast(
                    lat=self.coordinates[0],
                    lon=self.coordinates[1],
                    language=self.language,
                )
        else:
            raise YrException('location_name or location_xyz parameter must be set')

        self.connect = Connect(location=self.location)
        self.xml_source = None
        self.dictionary = None
        self.credit = self.language.dictionary['credit']

    async def data(self):
        if self.dictionary is None:
            self.xml_source = await self.connect.read()
            self.dictionary = self.xml2dict(self.xml_source)
        return self.dictionary

async def main():
    logging.info('starting __main__')

    weatherdata = await Yr(
        location_name='Czech_Republic/Prague/Prague',
        forecast_link='forecast',
        language_name='en',
    ).now(as_json=True)
    # print(weatherdata)

    weatherdata = await Yr(
        location_name='Czech_Republic/Prague/Prague',
        forecast_link='forecast_hour_by_hour',
        language_name='en',
    ).now(as_json=True)
    # print(weatherdata)

    weatherdata = await Yr(
        location_xyz=(14.4656239, 50.0596696, 11),
        language_name='en',
    ).now(as_json=True)
    # print(weatherdata)

    weatherdata = await Yr(
        coordinates=(50.0596696, 14.4656239, 11),
        language_name='en',
    ).now(as_json=True)
    # print(weatherdata)

    weatherdata = await Yr(
        coordinates=(63.4066631, 10.4426724, 10),
        language_name='en'
    ).now(as_json=True)
    # print(weatherdata)

    logging.info('stopping __main__')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())