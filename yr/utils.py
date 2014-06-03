#!/usr/bin/env python3

import os.path
import json # Language
import tempfile # Cache
import datetime # Cache
import urllib.request # Connect
import sys

class YrObject: encoding = 'utf-8'

class YrException(YrObject):

    def __init__(self, error_message):
        sys.stderr.write('python-yr: {error_message}\n'.format(error_message=error_message))
        sys.exit(1)

class Language(YrObject):

    script_directory = os.path.dirname(os.path.abspath(__file__)) # directory of the script
    directory = 'languages'

    def __init__(self, language_name='en'):
        self.language_name = language_name
        self.filename = os.path.join(
            self.script_directory,
            self.directory,
            '{root}.{ext}'.format(root=self.language_name, ext='json') # basename of filename
        )
        self.dictionary = self.get_dictionary()

    def get_dictionary(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', encoding=self.encoding) as f:
                return json.load(f)
        else:
            YrException('unavailable language ~> {language_name}'.format(language_name=self.language_name))

class Location(YrObject):

    def __init__(self, location_name, language_name='en'):
        self.location_name = location_name
        self.language_name = language_name
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        language = Language(self.language_name)
        url = 'http://www.yr.no/{place}/{location_name}/{forecast}.xml'.format(
            location_name = self.location_name,
            **language.dictionary # **language.dictionary contain ~> place + forecast
        )
        return url

    def get_hash(self):
        return self.location_name.replace('/', '-')

class Connect(YrObject):

    extension = 'weatherdata.xml'

    def __init__(self, location_name, language_name='en'):
        self.location_name = location_name
        self.language_name = language_name

    def read(self):
        location = Location(self.location_name, self.language_name)
        cache = Cache(location, self.extension)
        if not cache.exists() or not cache.is_fresh():
            response = urllib.request.urlopen(location.url)
            if response.status != 200:
                YrException('unavailable url ~> {url}'.format(url=location.url))
            weatherdata = response.read().decode(self.encoding)
            cache.dump(weatherdata)
        else:
            weatherdata = cache.load()
        return weatherdata

class Cache(YrObject):

    directory = tempfile.gettempdir()
    timeout = 30 # cache timeout in minutes

    def __init__(self, location, what):
        self.filename = os.path.join(
            self.directory,
            '{root}.{ext}'.format(root=location.hash, ext=what) # basename of filename
        )

    def dump(self, data):
        with open(self.filename, mode='w', encoding=self.encoding) as f:
            f.write(data)

    def is_fresh(self):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))
        now = datetime.datetime.now()
        timeout = datetime.timedelta(minutes=self.timeout)
        return mtime - now <= timeout

    def exists(self):
        return os.path.isfile(self.filename)

    def load(self):
        with open(self.filename, mode='r', encoding=self.encoding) as f:
            return f.read()

if __name__ == '__main__':
    print(Connect('Czech_Republic/Prague/Prague').read())
