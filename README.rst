=========
python-yr
=========

Asynchronous library for the norwegian weather service YR.no_ in Python_. Forked from python-yr_ by wkcd_. 

Usage
=====

.. code:: python

    from ayr.libayr import Yr

    weather = Yr(location_name='Norge/Telemark/Skien/Skien')
    now = await weather.now(as_json=True)

    print(now)

This returns
============

.. code:: json

    {
        "@from": "2014-06-04T08:00:00", 
        "@to": "2014-06-04T12:00:00", 
        "@period": "1", 
        "symbol": {
            "@number": "3", 
            "@numberEx": "3", 
            "@name": "Partly cloudy", 
            "@var": "03d"
        }, 
        "precipitation": {
            "@value": "0", 
            "@minvalue": "0", 
            "@maxvalue": "0.1"
        }, 
        "windDirection": {
            "@deg": "159.4", 
            "@code": "SSE", 
            "@name": "South-southeast"
        }, 
        "windSpeed": {
            "@mps": "1.3", 
            "@name": "Light air"
        }, 
        "temperature": {
            "@unit": "celsius", 
            "@value": "13"
        }, 
        "pressure": {
            "@unit": "hPa", 
            "@value": "1012.1"
        }
    }


.. _YR.no: http://www.yr.no/
.. _Python: http://www.python.org/
.. _python-yr: https://github.com/wckd/python-yr/
.. -wkcd: https://github.com/wckd/python-yr/