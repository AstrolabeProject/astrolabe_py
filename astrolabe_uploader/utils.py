#
# Module to provide general utility functions for Astrolabe code.
#   Written by: Tom Hicks. 7/26/2018.
#   Last Modified: Refactor metadata key file handling here.
#
import os
import fnmatch

# Default text file of desired metadata keys, one per line
_DEFAULT_KEYS_FILE = "metadata-keys.txt"

# patterns for identifying FITS and gzipped FITS files
_FITS_PAT = "*.fits"
_GZFITS_PAT = "*.fits.gz"

def is_fits_file(fyl):
    """ Return True if the given file is FITS file, else False. """
    return (fnmatch.fnmatch(fyl, _FITS_PAT) or fnmatch.fnmatch(fyl, _GZFITS_PAT))

def filter_file_tree(root_dir):
    """ Generator to yield all FITS files in the file tree under the given root directory. """
    fits_pat = "*.fits"                     # pattern for identifying FITS files
    gzfits_pat = "*.fits.gz"                # pattern for identifying gzipped FITS files
    for root, dirs, files in os.walk(root_dir):
        for fyl in files:
            if (is_files_file(fyl)):
                file_path = os.path.join(root, fyl)
                yield file_path

def get_metadata_keys(options):
    """ Return a list of metadata keys to be extracted. """
    keyfile = options.get("keyfile")
    if (keyfile):
        with open(keyfile, "r") as mdkeys_file:
            return mdkeys_file.read().splitlines()
    else:
        return None
