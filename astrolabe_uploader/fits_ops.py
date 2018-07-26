#
# Module to view, extract, and/or verify metadata from one or more FITS files.
#   Written by: Tom Hicks. 4/24/2018.
#   Last Modified: Remove info and verify tasks.
#
import os
import sys
import warnings
from astropy.io import fits
from astrolabe_uploader.fits_meta import FitsMeta

# dictionary of alternates for standard FITS metadata keys
_ALTERNATE_KEYS_MAP = {
    "NAXIS1": "spatial_axis_1_number_bins",
    "NAXIS2": "spatial_axis_2_number_bins",
    "DATE-OBS": "start_time",
    "INSTRUME": "facility_name",
    "TELESCOP": "instrument_name",
    "OBSERVER": "obs_creator_name",
    "OBJECT": "obs_title"
}

# dictionary mapping CTYPE* key names to their associated CRVAL* key names
_CTYPES = { "CTYPE1": "CRVAL1",  "CTYPE2": "CRVAL2" }

# set of metadata keys to ignore when extracting metadata from FITS files
_IGNORE_KEYS = set([ "COMMENT", "HISTORY" ])


def fits_metadata(file_path, options={}):
    """ Return a list Metadatum tuples extracted from the given FITS file. """
    keys_subset = options.get("keys_subset")
    fm = FitsMeta(file_path, ignore_keys=_IGNORE_KEYS)
    metadata = _post_process_metadata(fm, keys_subset)
    return metadata


def _post_process_metadata(fm, keys_subset):
    """ Post process the accumulated metadata; handle a couple of special cases. """
    for item in fm.metadata():              # check all metadata items for special cases
        _handle_alternate_key(fm, item, keys_subset) # fm and key_subset modified by side-effect
        _handle_ctype_mapping(fm, item, keys_subset) # fm and key_subset modified by side-effect

    if (keys_subset):                       # if user requested only a subset of the metadata
        return fm.filter_by_keys(keys_subset) # filter the metadata by the keys subset
    else:
        return fm.metadata()                # else just return all the accumulated metadata


def _handle_alternate_key(fm, item, keys_subset):
    """ For items whose keys are listed in the alternate key table, duplicate the item
        but use the alternate keyword for the duplicated item. """
    item_key = item.keyword                 # keyword of this item
    alt_key = _ALTERNATE_KEYS_MAP.get(item_key) # try to get an alternate key for this item
    if (alt_key):                           # if an alternate key exists
        if (keys_subset):                   # if only a subset of keys requested
            if (item_key in keys_subset):   # and this item key is in that subset
                if (fm.copy_item(item_key, alt_key)): # copy standard item w/ alternate keyword
                    keys_subset.append(alt_key) # if copied, add alternate keyword to the subset
                else:                           # else copy failed: move on
                    pass
            else:                           # else key not in subset: ignore this item
                pass
        else:                               # else not using a subset, so copy item
            fm.copy_item(item_key, alt_key) # copy standard item w/ alternate keyword


def _handle_ctype_mapping(fm, item, keys_subset):
    """ If a metadata item has a CTYPE key, it holds the interpretation of a corresponding
        CRVAL metadata item. Add a new item with the 'interpretation' key and the CRVAL value.
        For CRVALs and how they relate to CTYPEs see https://fits.gsfc.nasa.gov/fits_standard.html
    """
    # if this item's key is a CTYPE key, then get the CRVAL key interpreted by this item:
    crval_key = _CTYPES.get(item.keyword)   # lookup this item's key in CTYPE dictionary
    if (crval_key):                         # if this item key is a CTYPE key
        if "RA" in item.value:              # if this CTYPE item's value contains RA
            interp_key = "right_ascension"     # the 'interpretation' of the CRVAL value
        elif "DEC" in item.value:           # else if this CTYPE item's value contains DEC
            interp_key = "declination"         # the 'interpretation' of the CRVAL value
        else:                               # we only handle these interpretations, so far
            interp_key = None

        if (interp_key):                    # if we have a workable intepretation
            copied = fm.copy_item(crval_key, interp_key) # copy CRVAL value w/ interpretation key
            if (copied and keys_subset):       # if only a subset of keys requested
                keys_subset.append(interp_key) # add the interpretation keyword to the subset
