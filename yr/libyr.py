#!/usr/bin/env python3
import sys
import json
import xmltodict # <~ the only external dependency
from utils import Connect, Location, Language, YrException

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

    def now(self, as_json=True): # default is return result as json ;)
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

    """
    def temperature(self):
        '''
        Get temperature from yr and return it.
        '''
        getlocation = Location(self.location_name, self.language).find()
        cache = Cache(getlocation, 'temperature')
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())
        data = Connect(getlocation).read()
        data = et.fromstring(data)
        out = {}
        for parent in data[5].iter('temperature'):
            if parent.attrib:
                out['data'] = parent.attrib
        out['credit'] = self.yr_credit
        cache.write(json.dumps(out))
        return out

    def wind_speed(self):
        '''
        Get wind speed from yr.
        '''
        getlocation = Location(self.location_name, self.language).find()
        cache = Cache(getlocation, 'windspeed')
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())
        data = Connect(getlocation).read()
        data = et.fromstring(data)
        out = {}
        for parent in data[5].iter('windSpeed'):
            if parent.attrib:
                out['data'] = parent.attrib
        out['credit'] = self.yr_credit
        cache.write(json.dumps(out))
        return out

    def wind_direction(self):
        '''
        Get wind direction from yr.
        '''
        getlocation = Location(self.location_name, self.language).find()
        cache = Cache(getlocation, 'wind_direction')
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())
        data = Connect(getlocation).read()
        data = et.fromstring(data)
        out = {}
        for parent in data[5].iter('windDirection'):
            if parent.attrib:
                out['data'] = parent.attrib
        out['credit'] = self.yr_credit
        cache.write(json.dumps(out))
        return out

    def forecast(self):
        getlocation = Location(self.location_name, self.language).find()
        cache = Cache(getlocation, 'forecast')
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())
        data = Connect(getlocation).read()
        data = et.fromstring(data)
        days = []
        for parent in data[5][0].iter('text'):
            for child in parent[0]:
                days.append({
                    'from': child.get('from'), 
                    'to': child.get('to'), 
                    child[0].tag: child[0].text, 
                    child[1].tag: child[1].text,
                })
        out = {}
        out['data'] = days
        out['credit'] = self.yr_credit
        cache.write(json.dumps(out))
        return out

    def observations(self):
        getlocation = Location(self.location_name, self.language).find()
        cache = Cache(getlocation, 'observations')
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())
        data = Connect(getlocation).read()
        data = et.fromstring(data)
        observations = {}
        observations['data'] = {}
        for parent in data[6].iter('weatherstation'):
            stno = parent.attrib['stno']
            observations['data'][stno] = parent.attrib
            for child in parent:
                tag = child.tag
                observations['data'][stno][tag] = child.attrib
        observations['credit'] = self.yr_credit
        cache.write(json.dumps(observations))
        return observations

    def location_info(self):
        getlocation = Location(self.location_name, self.language).find()
        cache = Cache(getlocation, 'location')
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())
        data = Connect(getlocation).read()
        data = et.fromstring(data)
        location_list = []
        location = {}
        for parent in data[0]:
            if parent.attrib:
                location_list.append(parent.attrib)
            else:
                location_list.append({
                    parent.tag: parent.text
                })
        location['data'] = location_list
        location['credit'] = self.yr_credit
        cache.write(json.dumps(location))
        return location
    """

if __name__ == '__main__':
    print(Yr('Czech_Republic/Prague/Prague').now())
