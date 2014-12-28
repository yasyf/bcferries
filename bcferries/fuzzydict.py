import collections
from fuzzywuzzy import process

class FuzzyDict(collections.MutableMapping):
  def __init__(self, *args, **kwargs):
    self.d = dict()
    self.update(dict(*args, **kwargs))

  def __getitem__(self, key):
    if key in self.d:
      return self.d[key]
    result = process.extractOne(key, self.d.keys())
    if result and result[1] > 50:
      return self.d[result[0]]
    else:
      raise KeyError(key)

  def __setitem__(self, key, value):
    self.d[key] = value

  def __delitem__(self, key):
    del self.d[key]

  def __iter__(self):
    return iter(self.d)

  def __len__(self):
    return len(self.d)

  def __str__(self):
    return str(self.d)

  def __repr__(self):
    return repr(self.d)
