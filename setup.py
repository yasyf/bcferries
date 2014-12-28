from setuptools import setup

VERSION = '0.0.2'

def readme():
  with open('README.md') as f:
    return f.read()

setup(
  name = 'bcferries',
  packages = ['bcferries'],
  version = VERSION,
  description = 'BC Ferries Python Library',
  long_description = readme(),
  author = 'Yasyf Mohamedali',
  author_email = 'yasyfm@gmail.com',
  url = 'https://github.com/yasyf/bcferries',
  download_url = 'https://github.com/yasyf/bcferries/tarball/' + VERSION,
  license = 'MIT',
  keywords = ['bc ferries', 'schedule'],
  install_requires = ['requests', 'beautifulsoup4', 'python-dateutil', 'functools32', 'fuzzywuzzy'],
  extras_require = {
    'Levenshtein': ['python-Levenshtein']
  }
)
