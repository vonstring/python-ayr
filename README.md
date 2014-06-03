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
    "time": {
        "@from": "2014-02-08T21:00:00", 
        "@period": "3", 
        "@to": "2014-02-09T00:00:00", 
        "symbol": {
            "@name": "Rain", 
            "@number": "9", 
            "@var": "09"
        }, 
        "precipitation": {
            "@maxvalue": "6.2", 
            "@minvalue": "3.0", 
            "@value": "4.6"
        }, 
        "winddirection": {
            "@code": "SSE", 
            "@deg": "148.4", 
            "@name": "South-southeast"
        }, 
        "windspeed": {
            "@mps": "6.6", 
            "@name": "Moderate breeze"
        }, 
        "temperature": {
            "@unit": "celsius", 
            "@value": "3"
        }, 
        "pressure": {
            "@unit": "hPa", 
            "@value": "983.0"
        }
    }
}
```

More to come!
