"""
Class to extract and format metadata from FITS files.
  Last Modified: Rename Metadatum tuple. Use accessor methods.
"""
__version__ = "0.0.1"
__author__ = "Tom Hicks"

import collections
import logging
import warnings
from astropy.io import fits

logging.basicConfig(level=logging.ERROR)    # default logging configuration

Metadatum = collections.namedtuple('Metadatum', ['keyword', 'value'])

class FitsMeta:
    """ Class to extract and format metadata from FITS files. """

    def __init__(self, filename):
        self._filename = filename
        hdulist = fits.open(self._filename) # raises error if unable to read file
        hdu0 = hdulist[0]                   # get first HDU
        hdu0.verify('silentfix+ignore')     # fix fixable items in the first HDU
        self._metadata = [Metadatum(c[0], c[1]) for c in hdu0.header.items() if(c[0] and c[1])]
        hdulist.close()                     # close the file

    def __enter__(self):
        return self

    def __iter__(self):
        for md in self._metadata:
            yield md

    def __len__(self):
        return len(self._metadata)

    def filename(self):
        """ Return the filename of the file used by this class. """
        return self._filename

    def metadata(self):
      """ Return the metadata items. """
      return self._metadata
