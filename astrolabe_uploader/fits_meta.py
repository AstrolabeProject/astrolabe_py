"""
Class to extract and format metadata from FITS files.
  Last Modified: Initial creation.
"""
__version__ = "0.0.1"
__author__ = "Tom Hicks"

import collections
import logging
import warnings
from astropy.io import fits

logging.basicConfig(level=logging.ERROR)    # default logging configuration

Metadata = collections.namedtuple('Metadata', ['keyword', 'value'])

class FitsMeta:
    """ Class to extract and format metadata from FITS files. """

    def __init__(self, filename):
        self.filename = filename
        hdulist = fits.open(filename)       # raises error if unable to read file
        hdu0 = hdulist[0]                   # get first HDU
        hdu0.verify('silentfix+ignore')     # fix the first HDU
        self.metadata = [Metadata(c[0], c[1]) for c in hdu0.header.items()]
        hdulist.close()                     # close the file

    def __enter__(self):
        return self

    def __len__(self):
        return len(self.metadata)

    def filename(self):
        """ Return the filename of the file used by this class. """
        return self.filename

    def metadata(self):
      """ Return the metadata items. """
      return self.metadata
