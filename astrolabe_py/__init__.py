__version__ = "0.0.12"

import collections

# class to hold an individual metadatum, a list of which is the metadata
Metadatum = collections.namedtuple('Metadatum', ['keyword', 'value'])
