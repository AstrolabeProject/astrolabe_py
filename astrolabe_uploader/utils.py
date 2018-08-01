#
# Module to provide general utility functions for Astrolabe code.
#   Written by: Tom Hicks. 7/26/2018.
#   Last Modified: Refactor out FITS file patterns and test method.
#
import os
import fnmatch

_FITS_PAT = "*.fits"                        # pattern for identifying FITS files
_GZFITS_PAT = "*.fits.gz"                   # pattern for identifying gzipped FITS files

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
