# BC Ferries Python Library

This is the Python client library for interacting with information published to the [BC Ferries mobile site](http://mobile.bcferries.com/). It is essentially a wrapper around a BeautifulSoup scraper.

## Installation

`pip install bcferries`

## Usage

```python
from bcferries import BCFerries

bc = BCFerries()
terminals = bc.terminals()
# {u'Horseshoe Bay': BCFerriesTerminal (Horseshoe Bay), u'Tsawwassen': BCFerriesTerminal (Tsawwassen)}
t = terminals['Tsawwassen']
#BCFerriesTerminal (Tsawwassen)

routes = t.routes()
# {u'Tsawwassen to Duke Point': BCFerriesRoute (Tsawwassen to Duke Point)}
r = routes['Tsawwassen to Duke Point']
# BCFerriesRoute (Tsawwassen to Duke Point)

crossing = r.crossings()['10:45pm']
# BCFerriesCrossing (Tsawwassen to Duke Point at 5:45pm)
crossing.capacity
# BCFerriesCapacity (62% Full)
```

All returned dictionaries have fuzzy string matching on they keys.

```python
routes['Tsawwassen to Duke Point'] == routes['Tsaw to DP']
# True
```


`bcferries` caches the last eight API calls by default. You can change this to any integer you want.

```python
import bcferries.api

bcferries.api.BCFerriesAPI.cache_last = 16
```

You can also pass any function the `ignore_cache` keyword argument to bypass the cache.
