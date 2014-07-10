#!/usr/bin/env python3

import sys
import os.path
import json # Language
import tempfile # Cache
import datetime # Cache
import urllib.request # Connect
import urllib.parse # Location
import re

class YrObject: encoding = 'utf-8'

class YrException(Exception):
    pass

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
            raise YrException('unavailable language ~> {language_name}'.format(language_name=self.language_name))

class Location(YrObject):

    def __init__(self, location_name, forecast_link='forecast', language=Language()):
        self.location_name = location_name
        self.forecast_link = forecast_link
        self.language = language
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        url = 'http://www.yr.no/{place}/{location_name}/{forecast_link}.xml'.format(
            location_name = urllib.parse.quote(self.location_name),
            forecast_link = urllib.parse.quote(self.forecast_link),
            **self.language.dictionary # **self.language.dictionary contain ~> place + forecast_link
        )
        return url

    def get_hash(self):
        return self.location_name.replace('/', '-')

class LocationXYZ(YrObject):
    """Class to use the API of yr.no"""

    def __init__(self, x, y, z=0, language=Language()):
        """
        :param double x: longitude coordinate
        :param double y: latitude coordinate
        :param double z: altitude (meters above sea level)
        :param language: a Language object
        """
        self.x = x
        self.y = y
        self.z = z
        self.language = language
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        """Return the url of API service"""
        url = "http://api.yr.no/weatherapi/locationforecast/1.9/?lat={y};" \
              "lon={x};msl={z}".format(x=self.x, y=self.y, z=self.z)
        return url

    def get_hash(self):
        """Create an hash with the three coordinates"""
        return "location_{x}_{y}_{z}".format(x=self.x, y=self.y, z=self.z)

class Connect(YrObject):

    def __init__(self, location):
        self.location = location

    def read(self):
        cache = Cache(self.location)
        if not cache.exists() or not cache.is_fresh():
            try:
                response = urllib.request.urlopen(self.location.url)
            except:
                raise YrException('unavailable url ~> {url}'.format(url=self.location.url))
            if response.status != 200:
                raise YrException('unavailable url ~> {url}'.format(url=self.location.url))
            weatherdata = response.read().decode(self.encoding)
            cache.dump(weatherdata)
        else:
            weatherdata = cache.load()
        return weatherdata

class Cache(YrObject):

    directory = tempfile.gettempdir()
    extension = 'weatherdata.xml'
    timeout = 30 # cache timeout in minutes

    def __init__(self, location):
        self.location = location
        self.filename = os.path.join(
            self.directory,
            '{root}.{ext}'.format(root=self.location.hash, ext=self.extension) # basename of filename
        )

    def dump(self, data):
        with open(self.filename, mode='w', encoding=self.encoding) as f:
            f.write(data)

    def is_fresh(self):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))
        now = datetime.datetime.now()
        timeout = datetime.timedelta(minutes=self.timeout)
        return now - mtime <= timeout # thanks for the fix antorweep

    def exists(self):
        return os.path.isfile(self.filename)

    def load(self):
        with open(self.filename, mode='r', encoding=self.encoding) as f:
            return f.read()

class YrCSV:

    def __init__(self, forecast, parameters=['precipitation', 'windDirection',
                                             'windSpeed', 'temperature',
                                             'pressure'],
                 stats=['min', 'max', 'avg'], interval=[0, 6]):
        """YrCSV class to write CSV file for data returned by yr.no services

        :param dict forecast: the dictionary with values returner by yr.no
                              services, from function Yr.forecast of libyr.py
        :param list stats: a list with statistical value to calculate, admited
                           values are: 'min', 'max', 'avg'
        :param list interval: list of forecast interval to use, 0 has be set
                              everytime as first element, other options are:
                              3 for the three hours precipitation forecast,
                              6 for the six hours precipitation forecast
        :param list parameters: list of parameters to save in the CSV file.....
        """
        self.dictionary = forecast
        self.parameters = parameters
        self.accepted_interval = interval
        self.statistics = stats

    def _str2time(self, value):
        """Return datetime object from string

        :param str value: The string of datetime in the format
        """
        return datetime.datetime(*map(int, re.split('[^\d]', value)[:-1]))

    def _check_diff_time(self, record):
        """Return the interval between two observations

        :param dict record: the dictionary containing the values of a forecast
                            record
        """
        delta = self._str2time(record['@to']) - self._str2time(record['@from'])
        return delta.total_seconds() // 3600

    def _empty_dict(self):
        """Return a dictionary with parameters"""
        values = {}
        for p in self.parameters:
            values[p] = []
        return values

    def _mean(self, vals):
        """Calculate mean value of a list

        :param list vals: a list of values to calculate mean
        """
        return sum(vals) / len(vals)

    def _fill_dict(self, record):
        """Fill the dictionary with values of one record

        :param dict record: the dictionary containing the values of a forecast
                            record
        """
        for p in self.parameters:
            if p in record.keys():
                if '@value' in record[p].keys():
                    self.values[p].append(float(record[p]['@value']))
                elif '@percent' in record[p].keys():
                    self.values[p].append(float(record[p]['@percent']))
                elif '@deg' in record[p].keys():
                    self.values[p].append(float(record[p]['@deg']))
                elif '@mps' in record[p].keys():
                    self.values[p].append(float(record[p]['@mps']))

    def _fill_list(self, record):
        """Fill the list with values of one record

        :param dict record: the dictionary containing the values of a forecast
                            record
        """
        for p in self.parameters:
            if p in record.keys():
                if '@value' in record[p].keys():
                    self.values.append(record[p]['@value'])
                elif '@percent' in record[p].keys():
                    self.values.append(record[p]['@percent'])
                elif '@deg' in record[p].keys():
                    self.values.append(record[p]['@deg'])
                elif '@mps' in record[p].keys():
                    self.values.append(record[p]['@mps'])
            else:
                self.values.append('0')

    def _write_dict(self, record, header):
        """Add the value to the list to write in the CSV file according the
        header

        :param dict record: the dictionary containing the values of a forecast
                            record
        :param list header: a list the the values of header to keep the useful
                            data
        """
        values = []
        for h in header:
            if h != 'precipitation':
                p, s = h.split('_')
                if s == 'min':
                    values.append(str(min(record[p])))
                elif s == 'max':
                    values.append(str(max(record[p])))
                elif s == 'avg':
                    values.append(str(self._mean(record[p])))
            else:
                values.append(str(sum(record[h])))
        return values

    def _check_output(self, out):
        if out:
            return open(out, 'w')
        else:
            return sys.stdout

    def append_parameter(self, parameter):
        """Add one parameter to parameters list to analyze

        :param str parameter: the value of parameter to add to parameters list
        """
        self.parameters.append(parameter)

    def extend_parameters(self, parameters):
        """Add more parameters to parameters list to analyze

        :param list parameters: a list of parameters to add to parameters list
        """
        self.parameters.extend(parameters)

    def create_header(self, stats=False):
        """Create the header of CSV file with the name of parameter, the date
        is insert later because the header is used to query data"""
        header = []
        if stats:
            for p in self.parameters:
                if p != 'precipitation':
                    for s in self.statistics:
                        header.append("{par}_{stat}".format(par=p, stat=s))
                else:
                    header.append(p)
        else:
            header = self.parameters
        return header

    def return_daily(self):
        """Function to return a list with a values for each day

        :param str output: the complete path where write a csv file
        """
        header = self.create_header(True)
        oldate = None
        self.values = self._empty_dict()
        out_vals = []
        for forecast in self.dictionary:
            date = self._str2time(forecast['@to'])
            interval = self._check_diff_time(forecast)
            if not oldate:
                oldate = date.date()
            elif oldate != date.date():
                vals = [oldate.isoformat()]
                vals.extend(self._write_dict(self.values, header))
                #of.write("{date},{head}\n".format(date=oldate,
                         #head=",".join(vals)))
                out_vals.append(vals)
                oldate = date.date()
                self.values = self._empty_dict()
            if interval in self.accepted_interval:
                try:
                    self._fill_dict(forecast['location'])
                except:
                    self._fill_dict(forecast)
        return out_vals

    def return_all(self):
        """Function to return a list with all values of services"""
        out_vals = []
        for forecast in self.dictionary:
            interval = self._check_diff_time(forecast)
            if interval in self.accepted_interval:
                self.values = [forecast['@from'], forecast['@to']]
                try:
                    self._fill_list(forecast['location'])
                except:
                    self._fill_list(forecast)
                out_vals.append(self.values)
        return out_vals

    def write(self, outputfile, daily=False):
        """Write the CSV file

        :param str outputfile: the complete path where write a csv file
        :param bool daily: to choose if call return_all or return_daily function
        """
        of = self._check_output(outputfile)
        if daily:
            header = self.create_header(True)
            of.write("date,{head}\n".format(head=",".join(header)))
            vals = self.return_daily()
        else:
            header = self.create_header()
            of.write("fromdate,todate,{head}\n".format(head=",".join(header)))
            vals = self.return_all()
        for val in vals:
            of.write("{data}\n".format(data=",".join(val)))
        if outputfile:
            of.close

if __name__ == '__main__':
    print(Connect(Location(location_name='Czech_Republic/Prague/Prague')).read())
