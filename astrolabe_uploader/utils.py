#
# Module to provide general utility functions for Astrolabe code.
#   Written by: Tom Hicks. 7/26/2018.
#   Last Modified: Initial creation by aggregation of existing pieces.
#
import os
import fnmatch

def filter_file_tree(root_dir):
    """ Generator to yield all FITS files in the file tree under the given root directory. """
    fits_pat = "*.fits"                     # pattern for identifying FITS files
    gzfits_pat = "*.fits.gz"                # pattern for identifying gzipped FITS files
    for root, dirs, files in os.walk(root_dir):
        for fyl in files:
            if (fnmatch.fnmatch(fyl, fits_pat) or fnmatch.fnmatch(fyl, gzfits_pat)):
                file_path = os.path.join(root, fyl)
                yield file_path
