# BC Ferries Python Library

This is the Python client library for interacting with information published to the [BC Ferries mobile site](http://mobile.bcferries.com/). It is essentially a wrapper around a BeautifulSoup scraper.

## Installation

`pip install bcferries`

## Usage

```python
from bcferries.bcferries import BCFerries

bc = BCFerries()
terminals = bc.terminals()
t = terminals['Tsawwassen']

routes = t.routes()
r = routes['Tsawwassen to Duke Point']

crossing = r.crossings()['10:45pm']
print crossing.capacity
```
