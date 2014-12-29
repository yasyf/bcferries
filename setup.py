from setuptools import setup

execfile('bcferries/version.py')

def readme():
  # Generated with `pandoc --from=markdown --to=rst --output=README.rst README.md`
  with open('README.rst') as f:
    return f.read()

setup(
  name = 'bcferries',
  packages = ['bcferries'],
  version = VERSION,
  description = 'BC Ferries Python Library',
  long_description = readme(),
  author = 'Yasyf Mohamedali',
  author_email = 'yasyfm@gmail.com',
  url = 'http://yasyf.github.io/bcferries/',
  download_url = 'https://github.com/yasyf/bcferries/tarball/' + VERSION,
  license = 'MIT',
  keywords = ['bc ferries', 'schedule'],
  install_requires = [
    'requests',
    'beautifulsoup4',
    'python-dateutil',
    'functools32',
    'python-Levenshtein',
    'geopy'
  ],
  classifiers= [
    'License :: OSI Approved :: MIT License',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4'
  ],
  use_2to3 = True
)
