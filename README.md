python-yr
=================
Library for the norwegian wheather service yr.no in python.

Pull requests are very welcomed! :-)

### Usage
```python
from yr.libyr import Yr

weather = Yr('Norge/Telemark/Skien/Skien')
now_json = weather.now(as_json=True)
# now = weather.now() # returns a dict

print(now_json)
```

### This returns
```json
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
```

More to come!
