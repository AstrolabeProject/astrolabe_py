"""
Class to extract and format metadata from FITS files.
  Last Modified: Move as_json and filter_by_* methods to module scope.
"""
__version__ = "0.0.4"
__author__ = "Tom Hicks"

import collections
import json
import logging
import re
import warnings
from astropy.io import fits

logging.basicConfig(level=logging.ERROR)    # default logging configuration

# class to hold an individual metadatum, a list of which is the metadata
Metadatum = collections.namedtuple('Metadatum', ['keyword', 'value'])

def as_json(metadata):
    """ Format and return the given metadata as a JSON string. """
    return json.dumps(metadata)

def default_cleaner_fn(fld):
    """ Return a copy of the given field cleaned up by removing any unwanted characters. """
    if (isinstance(fld, str)):
        return re.sub("[\"\'\\\\]", "", fld) # remove quotes and backslashes
    else:
        return fld

def filter_by_fn(metadata, predicate=None):
    """ Return a list of Metadatum items passing the given filter predicate.
        If filter predicate is not given, the identity function is assumed
        and all elements of iterable that are false are removed.
    """
    return list(filter(predicate, metadata))

def filter_by_keys(metadata, keys):
    """ Return a list of Metadatum items whose keys are in the given metadata. """
    return filter_by_fn(metadata, lambda item: item.keyword in set(keys))

def key_set(metadata):
    """ Return a list of the keys for the given metadata. """
    return set([item.keyword for item in metadata])


class FitsMeta:
    """ Class to extract and format metadata from FITS files. """

    FILEPATH_KEY = "filepath"

    def __init__(self, filepath, cleaner=default_cleaner_fn):
        self._filepath = filepath
        hdulist = fits.open(self._filepath) # raises error if unable to read file
        self._hdusinfo = hdulist.info(False) # get summary info for all HDUs
        hdu0 = hdulist[0]                   # get first HDU
        hdu0.verify('silentfix+ignore')     # fix fixable items in the first HDU
        self._metadata = self._extract_metadata(hdu0.header, cleaner)
        self._metadata.append(Metadatum(self.FILEPATH_KEY, self._filepath))
        self._key_set = key_set(self._metadata)
        hdulist.close()                     # close the file

    def __enter__(self):
        return self

    def __contains__(self, keyword):
        return keyword in self._key_set

    def __iter__(self):
        for md in self._metadata:
            yield md

    def __len__(self):
        return len(self._metadata)


    def filepath(self):
        """ Return the filepath of the file used by this class. """
        return self._filepath

    def hdu_info(self):
        """ Return summary info for all HDUs in the input file. """
        return self._hdusinfo

    def key_set(self):
        """ Return the set of keywords for the metadata items. """
        return self._key_set

    def metadata(self):
        """ Return the metadata items. """
        return self._metadata

    def metadata_for_keys(self, keys=None):
        """ Return a list of metadata items with the specified keys or
            all items, if no keys are specified.
        """
        ks = self._key_set
        if (keys):
            ks = set(keys)
        return filter_by_keys(self._metadata, ks)

    def metadata_as_json(self):
        """ Return the metadata items as JSON. """
        return as_json(self._metadata)


    def _extract_metadata(self, header, cleaner):
        """ Return a list of metadata pairs, extracted and cleaned from the given FITS Header. """
        metadata = []
        for k, v in header.items():
            key = cleaner(k)
            val = cleaner(v)
            if (key and val):
                metadata.append(Metadatum(key, val))
        return metadata
