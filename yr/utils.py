#!/usr/bin/env python3

from __future__ import with_statement
import logging
import sys
import os.path
import json # Language
import tempfile # Cache
import datetime # Cache
import requests # Connect
import urllib2, urllib, urlparse # Location
from io import open

class YrObject(object):

    script_directory = os.path.dirname(os.path.abspath(__file__)) # directory of the script
    encoding = u'utf-8'

class YrException(Exception):

    def __init__(self, message):
        logging.error(message)
        raise

class Language(YrObject):

    directory = u'languages'
    default_language_name = u'en'
    extension = u'json'

    def __init__(self, language_name=default_language_name):
        self.language_name = language_name
        self.filename = os.path.join(
            self.script_directory,
            self.directory,
            u'{language_name}.{extension}'.format(
                language_name = self.language_name,
                extension = self.extension,
            ), # basename of filename
        )
        self.dictionary = self.get_dictionary()

    def get_dictionary(self):
        try:
            logging.info(u'read language dictionary: {}'.format(self.filename))
            with open(self.filename, mode=u'r', encoding=self.encoding) as f:
                return json.load(f)
        except Exception, e:
            raise YrException(e)

class Location(YrObject):

    base_url = u'http://www.yr.no/'
    default_forecast_link = u'forecast'
    forecast_links = [default_forecast_link, u'forecast_hour_by_hour']
    extension = u'xml'

    def __init__(self, location_name, forecast_link=default_forecast_link, language=False):
        self.location_name = location_name
        self.language = language if isinstance(language, Language) else Language()

        if forecast_link in self.forecast_links: # must be valid forecast_link
            self.forecast_link = self.language.dictionary[forecast_link]
        else:
            self.forecast_link = self.default_forecast_link

        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        return u'{base_url}{place}/{location_name}/{forecast_link}.{extension}'.format(
            base_url = self.base_url,
            place = self.language.dictionary[u'place'],
            location_name = urllib.quote(self.location_name),
            forecast_link = self.forecast_link,
            extension = self.extension,
        )

    def get_hash(self):
        return u'{location_name}.{forecast_link}'.format(
            location_name=self.location_name.replace(u'/', u'-'),
            forecast_link=self.forecast_link,
        )

class API_Locationforecast(YrObject):
    u"""Class to use the API of yr.no"""

    base_url = u'http://api.yr.no/weatherapi/locationforecast/1.9/?'
    forecast_link = u'locationforecast'

    def __init__(self, lat, lon, msl=0, language=False):
        u"""
        :param double lat: latitude coordinate
        :param double lon: longitude coordinate
        :param double msl: altitude (meters above sea level)
        :param language: a Language object
        """
        self.coordinates = dict(lat=lat, lon=lon, msl=msl)
        self.location_name = u'lat={lat};lon={lon};msl={msl}'.format(**self.coordinates)
        #self.language = language if isinstance(language, Language) else Language()
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        u"""Return the url of API service"""
        return u'{base_url}{location_name}'.format(
            base_url=self.base_url,
            location_name=self.location_name,
        )

    def get_hash(self):
        u"""Create an hash with the three coordinates"""
        return u'{location_name}.{forecast_link}'.format(
            location_name=self.location_name,
            forecast_link=self.forecast_link,
        )

class LocationXYZ(API_Locationforecast): # ~> Deprecated!!!
    u"""Class to use the API of yr.no"""

    def __init__(self, x, y, z=0, language=False):
        u"""
        :param double x: longitude coordinate
        :param double y: latitude coordinate
        :param double z: altitude (meters above sea level)
        :param language: a Language object
        """
        super(self.__class__, self).__init__(y, x, z, language)

class Connect(YrObject):

    def __init__(self, location):
        self.location = location

    def read(self):
        try:
            logging.info(u'weatherdata request: {}, forecast-link: {}'.format(
                self.location.location_name,
                self.location.forecast_link,
            ))
            cache = Cache(self.location)
            if not cache.exists() or not cache.is_fresh():
                logging.info(u'read online: {}'.format(self.location.url))
                response = requests.get(self.location.url)
                if response.status_code != 200:
                    raise
                weatherdata = response.text
                cache.dump(weatherdata)
            else:
                weatherdata = cache.load()
            return weatherdata
        except Exception, e:
            raise YrException(e)

class Cache(YrObject):

    directory = tempfile.gettempdir()
    extension = u'xml'
    timeout = 15 # cache timeout in minutes

    def __init__(self, location):
        self.location = location
        self.filename = os.path.join(
            self.directory,
            u'{location_hash}.{extension}'.format(
                location_hash=self.location.hash,
                extension=self.extension,
            ), # basename of filename
        )

    def dump(self, data):
        logging.info(u'write caching: {}'.format(self.filename))
        with open(self.filename, mode=u'w', encoding=self.encoding) as f:
            f.write(data)

    def is_fresh(self):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))
        now = datetime.datetime.now()
        timeout = datetime.timedelta(minutes=self.timeout)
        return now - mtime <= timeout # thanks for the fix antorweep

    def exists(self):
        return os.path.isfile(self.filename)

    def load(self):
        logging.info(u'read from cache: {}'.format(self.filename))
        with open(self.filename, mode=u'r', encoding=self.encoding) as f:
            return f.read()

if __name__ == u'__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info(u'starting __main__')

    weatherdata = Connect(Location(
        location_name=u'Czech_Republic/Prague/Prague',
        forecast_link=u'forecast',
        language=Language(language_name=u'en'),
    )).read()
    #print(weatherdata)

    weatherdata = Connect(Location(
        location_name=u'Czech_Republic/Prague/Prague',
        forecast_link=u'forecast_hour_by_hour',
        language=Language(language_name=u'en'),
    )).read()
    #print(weatherdata)

    weatherdata = Connect(API_Locationforecast(
        50.0596696,
        14.4656239,
        11,
        language=Language(language_name=u'en'),
    )).read()
    #print(weatherdata)

    logging.info(u'stopping __main__')
