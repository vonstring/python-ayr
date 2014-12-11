=========
python-yr
=========

Library for the norwegian wheather service yr.no_ in python_.

Usage
=====

.. code:: python

    from yr.libyr import Yr

    weather = Yr(location_name='Norge/Telemark/Skien/Skien')
    now = weather.now(as_json=True)

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

For more usage examples visit folder examples_ or project wiki_

Pull requests are very welcomed! :-)

.. _yr.no: http://www.yr.no/
.. _python: http://www.python.org/
.. _examples: https://github.com/wckd/python-yr/blob/master/yr/examples
.. _wiki: https://github.com/wckd/python-yr/wiki
