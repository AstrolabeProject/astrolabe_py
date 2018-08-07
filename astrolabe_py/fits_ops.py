#
# Module to view, extract, and/or verify metadata from one or more FITS files.
#   Written by: Tom Hicks. 4/24/2018.
#   Last Modified: Fix: bad options default.
#
import os
import sys
import warnings
from astropy.io import fits
import astrolabe_py.utils as utils
from astrolabe_py.fits_meta import FitsMeta

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


def execute_info(options):
    """ Returns a (possibly empty) list, each element of which is a list of
        summary information strings for the HDUs in a single FITS file.
    """
    # execute action for a single file or a directory of files
    file_path = options.get("images_path")
    if (os.path.isfile(file_path)):
        info = fits_hdu_info(file_path, options)
        return [info] if info else []
    else:
        if (os.path.isdir(file_path)):
            info_lst = [fits_hdu_info(fits_file, options)
                        for fits_file in utils.filter_file_tree(file_path)]
            return [info for info in info_lst if info] # just in case: remove empty lists
        else:                                          # should never happen
            print("Error: Specified file path '{}' is not a file or directory".format(file_path))
            sys.exit(20)

def fits_hdu_info(file_path, options={}):
    """ Return a list of summary information strings for the HDUs of the given FITS file. """
    verbose = options.get("verbose", False)
    if (verbose):
        print("Reading HDU information for file {} ...".format(file_path))
    fm = FitsMeta(file_path)
    hduinfo = fm.hdu_info()
    filename = os.path.basename(fm.filepath())
    # format the information into a report (a list of strings):
    results = ["Filename: {}".format(filename),
               "No.    Name      Ver    Type      Cards   Dimensions   Format"]
    layout = "{:3d}  {:10}  {:3} {:11}  {:5d}   {}   {}   {}"
    for hinfo in hduinfo:
        results.append(layout.format(*hinfo))
    return results


def fits_metadata(file_path, options={}):
    """ Return a list Metadatum tuples extracted from the given FITS file. """
    keys_subset = options.get("keys_subset")
    ignore_keys = options.get("ignore_keys")
    fm = FitsMeta(file_path, ignore_keys=ignore_keys)
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


def execute_verify(options):
    """ Returns a (possibly empty) list, each element of which is a list of
        warning strings from files which violate the FITS standard.
    """
    # execute action for a single file or a directory of files
    file_path = options.get("images_path")
    if (os.path.isfile(file_path)):
        warn = fits_verify(file_path, options)
        return [warn] if warn else []
    else:
        if (os.path.isdir(file_path)):
            warn_lst = [fits_verify(fits_file, options)
                        for fits_file in utils.filter_file_tree(file_path)]
            return [warn for warn in warn_lst if warn] # remove empty lists
        else:                                          # should never happen
            print("Error: Specified file path '{}' is not a file or directory".format(file_path))
            sys.exit(30)

def fits_verify(file_path, options={}):
    """ Verify that the data in the given FITS file conforms to the FITS standard.
        Return a (possibly empty) list of verification warning strings.
    """
    verbose = options.get("verbose", False)
    results = []
    with fits.open(file_path) as hdu:
        if (verbose):
            print("Checking file {} ...".format(file_path))
        with warnings.catch_warnings(record=True) as warns:
            hdu.verify("fix+warn")
            if (warns and len(warns) > 0):
                results.append("Filename: {}".format(file_path))
                for warn in warns:
                    results.append(str(warn.message))
    return results
