#
# Module to view, extract, and/or verify metadata from one or more FITS files.
#   Written by: Tom Hicks. 4/24/2018.
#   Last Modified: Port to Uploader.
#
import warnings
import sys
from astropy.io import fits

# Dictionary of alternates for standard FITS metadata keys
ALTERNATE_KEYS_MAP = {
'spatial_axis_1_number_bins': 'NAXIS1',
'spatial_axis_2_number_bins': 'NAXIS2',
'start_time': 'DATE-OBS',
'facility_name': 'INSTRUME',
'instrument_name': 'TELESCOP',
'obs_creator_name': 'OBSERVER',
'obs_title': 'OBJECT'
}
ALTERNATE_KEYS = set(ALTERNATE_KEYS_MAP.keys())
FILEPATH_KEY = 'filepath'

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
            elif ((key == 'CRVAL1') or (key == 'CRVAL2')):
                handle_ctype_mapping(key, file_metadata, metadata)
            else:                                           # just lookup the given key
                metadata.append( (key, file_metadata.get(key)) )
        except KeyError:
            metadata.append( (key, '') )
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
            hdu.verify('silentfix+ignore')
            hdr = hdu.header
            for key in hdr.keys():
                val = str(hdr[key])
                if (key and val):                   # ignore blank keys or values
                    print(key + ': ' + val)
        print()


def fits_verify(file_path, options=None):
    """Verify that the data in the given FITS file conforms to the FITS standard.
       Writes any verification warnings to the specified problem log file.
    """
    problems_file = "problems.txt"
    with fits.open(file_path) as hdu:
        with warnings.catch_warnings(record=True) as warns:
            hdu.verify('fix+warn')
            if (warns and len(warns) > 0):
                print("Filename: " + file_path)
                for warn in warns:
                    print(str(warn.message))


def get_metadata_keys(options):
    "Return a list of metadata keys to be extracted"
    keyfile = options.get("keyfile")
    with open(keyfile, 'r') as mdkeys_file:
        return mdkeys_file.read().splitlines()


def handle_ctype_mapping(key, file_metadata, metadata):
    """If key is a special value which provides the meaning of other fields, then
       add the key and its value and then write the referenced value with a another key.
       For CRVALs and how they relate to CRTYPEs see https://fits.gsfc.nasa.gov/fits_standard.html
    """
    if (key == 'CRVAL1'):
        metadata.append( ('CRVAL1', file_metadata.get('CRVAL1')) )
        if 'RA' in file_metadata['CTYPE1']:
            metadata.append( ('right_ascension', file_metadata.get('CRVAL1')) )
        elif 'DEC' in file_metadata['CTYPE1']:
            metadata.append( ('declination', file_metadata.get('CRVAL1')) )
        else:
            metadata.append( (key, '') )
    elif (key == 'CRVAL2'):
        metadata.append( ('CRVAL2', file_metadata.get('CRVAL2')) )
        if 'RA' in file_metadata['CTYPE2']:
            metadata.append( ('right_ascension', file_metadata.get('CRVAL2')) )
        elif 'DEC' in file_metadata['CTYPE2']:
            metadata.append( ('declination', file_metadata.get('CRVAL2')) )
        else:
            metadata.append( (key, '') )
