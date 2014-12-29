# BC Ferries Python Library

This is the Python client library for interacting with information published on the [BC Ferries mobile site](http://mobile.bcferries.com/). It is essentially a wrapper around a BeautifulSoup-powered scraper. Better documentation and tests are still in the works; feel free to contribute!

## Installation

`pip install bcferries`

## Setup

Some functions require interaction with a geocoding service; the Google Maps API is used for this. In order to prevent severe rate limiting, you'll want to acquire an API key. To let `bcferries` know about this key, set it as the `GOOGLE_MAPS_API_KEY` environment variable. Alternatively, you can pass it as an optional keyword argument to the constructor.

```python
from bcferries import BCFerries

bc = BCFerries(google_maps_api_key='xxx-xxx-xxx')
```

## Usage

```python
terminals = bc.terminals()
# {u'Horseshoe Bay': BCFerriesTerminal(Horseshoe Bay), u'Tsawwassen': BCFerriesTerminal(Tsawwassen)}
t = terminals['Tsawwassen']
# BCFerriesTerminal(Tsawwassen)

routes = t.routes()
# {u'Tsawwassen to Duke Point': BCFerriesRoute(Tsawwassen to Duke Point)}
r = routes['Tsawwassen to Duke Point']
# BCFerriesRoute(Tsawwassen to Duke Point)
r.distance()
# Distance(61.9591068557)

crossing = r.crossings()['10:45pm']
# BCFerriesCrossing(Tsawwassen to Duke Point at 5:45pm)
crossing.capacity
# BCFerriesCapacity(18% Full)
```

## Fuzzy Results

All returned dictionaries have fuzzy string matching on they keys.

```python
routes['Tsawwassen to Duke Point'] == routes['Tsaw to DP']
# True
```

There is also fuzzy time matching on keys that represent a nearby time.

```python
r = routes['HBay to DBay']
schedule = r.schedule()
schedule['6:12 PM']
# BCFerriesScheduledCrossing(Queen of Cowichan at 6:30 PM)
```

`datetime` objects can also be used as keys.

```python
from datetime import datetime

datetime.datetime.now()
# datetime.datetime(2014, 12, 28, 10, 42, 35, 630996)
schedule[datetime.datetime.now()]
# BCFerriesScheduledCrossing(Coastal Renaissance at 10:40 AM)
```

## Caching

`bcferries` caches the 16 most used API calls for up to five minutes by default. You can change this behavior as below. This must be done before creating a `BCFerries` object.

```python
import bcferries
import datetime

bcferries.set_cache_size(16)
bcferries.set_cache_timeout(datetime.timedelta(minutes=5))
```

You can also pass any function the `ignore_cache` keyword argument to bypass the cache, or call the `flush_cache` method on `BCFerries` to clear the entire cache.

```python
terminals = bc.terminals() # initial call takes multiple seconds
terminals = bc.terminals() # repeated call returns almost instantly
terminals = bc.terminals(ignore_cache=True) # takes multiple seconds to return

bc.flush_cache() # wipes the cache
```

## Export

You can export any subset of information with a call to `to_dict` on any object. You can also use `to_fuzzy_dict` and `to_json` as needed. To export all available information, call any of these methods on a `BCFerries` instance, and be prepared to wait a while.

```python
crossing.capacity
# BCFerriesCapacity(18% Full)
crossing.capacity.to_dict()
# {'passenger_filled': 32, 'mixed_filled': 4, 'name': '18% Full', 'filled': 18}
```
