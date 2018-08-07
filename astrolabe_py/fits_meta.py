"""
Class to extract and format metadata from FITS files.
  Last Modified: Update for project rename.
"""
import copy
import json
import logging
import re
import warnings
from astropy.io import fits
from astrolabe_py import Metadatum

logging.basicConfig(level=logging.ERROR)    # default logging configuration

FILEPATH_KEY = "filepath"

def default_cleaner_fn(fld):
    """ Return a copy of the given field cleaned up by removing any unwanted characters. """
    if (isinstance(fld, str)):
        return re.sub("[\"\'\\\\]", "", fld) # remove quotes and backslashes
    else:
        return fld


class FitsMeta:
    """ Class to extract and format metadata from FITS files. """

    def __init__(self, filepath, cleaner=default_cleaner_fn, ignore_keys=None):
        self._filepath = filepath
        hdulist = fits.open(self._filepath) # raises error if unable to read file
        self._hdusinfo = hdulist.info(False) # get summary info for all HDUs
        hdu0 = hdulist[0]                   # get first HDU
        hdu0.verify('silentfix+ignore')     # fix fixable items in the first HDU
        self._metadata = self._extract_metadata(hdu0.header, cleaner)
        self._metadata.append(Metadatum(FILEPATH_KEY, self._filepath))
        if (ignore_keys):
            self._metadata = self.remove_by_keys(ignore_keys)
        self._update_key_set()              # compute initial set of metadata keys
        hdulist.close()                     # close the file

    def __enter__(self):
        return self

    def __contains__(self, keyword):
        return keyword in self._key_set

    def __getitem__(self, keyword):
        item = self.get(keyword)
        if (item):
            return item
        raise KeyError("Key '{}' not found in this metadata".format(keyword))

    def __iter__(self):
        for item in self._metadata:
            yield item

    def __len__(self):
        return len(self._metadata)


    def copy_item(self, src_key, target_key, nodup=False):
        """ Copy an existing metadatum, named by the src_key, back into the metadata
            with a new key specified by target_key. If nodup flag is True, then the copy
            is prevented if it would create a duplicate of an existing metadata key.
            If the metadatum is successfully copied, the internal key set is updated.
            Returns True if metadatum copied, False otherwise.
        """
        copied = False
        src_entry = self.get(src_key)
        if (src_entry):
            if ((target_key not in self._key_set) or (not nodup)):  # if no target or dups allowed
                copy = src_entry._replace(keyword=target_key, value=src_entry.value)
                self._metadata.append(copy)
                self._update_key_set()
                copied = True
        return copied

    def filepath(self):
        """ Return the filepath of the file used by this class. """
        return self._filepath

    def filter_by_keys(self, keys):
        """ Return a list of Metadatum items whose keys are in the given key set. """
        return list(filter(lambda item: item.keyword in set(keys), self._metadata))

    def get(self, keyword, not_found=None):
        """ Return the first metadatum with the given key or the not_found value, if
            an entry with the specified key is not present in the metadata.
        """
        if (type(keyword) != str):
            raise TypeError("The key for metadata items must be a string")
        if (keyword in self._key_set):
            for item in self._metadata:
                if (item.keyword == keyword):
                    return item
        return not_found

    def hdu_info(self):
        """ Return summary info for all HDUs in the input file. """
        return self._hdusinfo

    def key_set(self):
        """ Return the set of keywords for the metadata items. """
        return copy.copy(self._key_set)

    def metadata(self):
        """ Return the metadata items. """
        return copy.copy(self._metadata)

    def metadata_for_keys(self, keys=None):
        """ Return a list of metadata items with the specified keys or
            all items, if no keys are specified.
        """
        ks = self._key_set
        if (keys):
            ks = set(keys)
        return self.filter_by_keys(ks)

    def metadata_as_json(self):
        """ Return the metadata items as JSON. """
        return json.dumps(self._metadata)

    def remove_by_keys(self, keys):
        """ Return a list of Metadatum items whose keys are NOT in the given key set. """
        return list(filter(lambda item: item.keyword not in set(keys), self._metadata))


    def _extract_metadata(self, header, cleaner):
        """ Return a list of metadata pairs, extracted and cleaned from the given FITS Header. """
        metadata = []
        for k, v in header.items():
            key = str(cleaner(k))           # clean key and ensure it is a string
            val = str(cleaner(v))           # clean value and ensure it is a string
            if (key and val):
                metadata.append(Metadatum(key, val))
        return metadata

    def _update_key_set(self):
        """ Recompute and save the list of keys for the current metadata. """
        self._key_set = set([item.keyword for item in self._metadata])
