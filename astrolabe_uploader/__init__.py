__version__ = "0.0.10"
__author__ = "Tom Hicks"

import collections

# class to hold an individual metadatum, a list of which is the metadata
Metadatum = collections.namedtuple('Metadatum', ['keyword', 'value'])
