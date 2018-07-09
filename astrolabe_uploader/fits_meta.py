#
# Module to view, extract, and/or verify metadata from one or more FITS files.
#   Written by: Tom Hicks. 4/24/2018.
#   Last Modified: Redo handle for ctype mapping. Consistent quotes.
#
import warnings
import sys
from astropy.io import fits

# dictionary of alternates for standard FITS metadata keys
ALTERNATE_KEYS_MAP = {
"spatial_axis_1_number_bins": "NAXIS1",
"spatial_axis_2_number_bins": "NAXIS2",
"start_time": "DATE-OBS",
"facility_name": "INSTRUME",
"instrument_name": "TELESCOP",
"obs_creator_name": "OBSERVER",
"obs_title": "OBJECT"
}
ALTERNATE_KEYS = set(ALTERNATE_KEYS_MAP.keys())

# dictionary mapping CRVALs to their interpretation items
CRVALS = { "CRVAL1": "CTYPE1", "CRVAL2": "CTYPE2" }
CRVAL_KEYS = set(CRVALS.keys())

FILEPATH_KEY = "filepath"

def extract_metadata(file_path, hdu, desired_keys):
    """Extract the metadata from the HeaderDataUnit of the given file for the keys
       in the given list of sought keys. Return a list of metadata key/value tuples."""
    file_metadata = hdu[0].header
    metadata = []                                   # return list of metadata key/value tuples
    for key in desired_keys:
        try:
            if (key == FILEPATH_KEY):                       # special case: include file path
                metadata.append( (FILEPATH_KEY, str(file_path)) )
            elif (key in ALTERNATE_KEYS):                   # is this an alternate key?
                standard_key = ALTERNATE_KEYS_MAP[key]      # get more standard key
                metadata.append( (key, file_metadata.get(standard_key)) )
            elif (key in CRVAL_KEYS):
                handle_ctype_mapping(key, file_metadata, metadata)
            else:                                           # just lookup the given key
                metadata.append( (key, file_metadata.get(key)) )
        except KeyError:
            metadata.append( (key, "") )
    return metadata


def fits_metadata(file_path, options):
    "Return a list of key/value metadata tuples (strings) extracted from the given FITS file"
    desired_keys = get_metadata_keys(options)
    with fits.open(file_path) as hdu:
        metadata = extract_metadata(file_path, hdu, desired_keys)
    # filter out any metadata key/value pairs without values
    return [mdata for mdata in metadata if mdata[1]]


def fits_info(file_path, options=None):
    "Print the Header Data Unit information for the given FITS file"
    with fits.open(file_path) as hdus:
        print(hdus.info())
        for hdu in hdus:
            hdu.verify("silentfix+ignore")
            hdr = hdu.header
            for key in hdr.keys():
                val = str(hdr[key])
                if (key and val):                   # ignore blank keys or values
                    print(key + ": " + val)
        print()


def fits_verify(file_path, options=None):
    """Verify that the data in the given FITS file conforms to the FITS standard.
       Writes any verification warnings to the specified problem log file.
    """
    problems_file = "problems.txt"
    with fits.open(file_path) as hdu:
        with warnings.catch_warnings(record=True) as warns:
            hdu.verify("fix+warn")
            if (warns and len(warns) > 0):
                print("Filename: " + file_path)
                for warn in warns:
                    print(str(warn.message))


def get_metadata_keys(options):
    "Return a list of metadata keys to be extracted"
    keyfile = options.get("keyfile")
    with open(keyfile, "r") as mdkeys_file:
        return mdkeys_file.read().splitlines()


def handle_ctype_mapping(key, file_metadata, metadata):
    """ If a metadata item has a CRVAL* key, it holds a value whose interpretation is defined
        by a corresponding CTYPE* metadata item. Add the base CRVAL item and then add another
        item with an interpretated key and the CRVAL value.
        For CRVALs and how they relate to CTYPEs see https://fits.gsfc.nasa.gov/fits_standard.html
    """
    ctype_key = CRVALS.get(key)             # get CTYPE* key interpreting the CRVAL* item
    if (ctype_key):                         # sanity check: CRVAL* key must be CRVALS dictionary
        metadata.append( (key, file_metadata.get(key)) )
        if "RA" in file_metadata[ctype_key]:
            metadata.append( ("right_ascension", file_metadata.get(key)) )
        elif "DEC" in file_metadata[ctype_key]:
            metadata.append( ("declination", file_metadata.get(key)) )
        else:                               # we only handle these interpretations, so far
            pass
