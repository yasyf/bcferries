# BC Ferries Python Library

This is the Python client library for interacting with information published to the [BC Ferries mobile site](http://mobile.bcferries.com/). It is essentially a wrapper around a BeautifulSoup scraper.

## Installation

`pip install bcferries`

## Usage

```python
from bcferries import BCFerries

bc = BCFerries()
terminals = bc.terminals()
t = terminals['Tsawwassen']

routes = t.routes()
r = routes['Tsawwassen to Duke Point']

crossing = r.crossings()['10:45pm']
print crossing.capacity
```


`bcferries` caches the last five API calls by default. You can change this by setting `bcferries.api.BCFerriesAPI.cache_last`. You can also pass any function the `ignore_cache` keyword argument to bypass the cache.
