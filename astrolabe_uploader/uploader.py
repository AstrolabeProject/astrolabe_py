#
# Module to extract metadata and upload one or more FITS files to iRods.
#   Written by: Tom Hicks. 7/19/2018.
#   Last Modified: Initial working version of do_file.
#
import os
import sys
import logging
import fnmatch

import astrolabe_uploader.fits_ops as fo
import astrolabe_uploader.irods_help as ih

logging.basicConfig(level=logging.INFO)     # default logging configuration

_ASTROLABE_ROOT_DIR = "astrolabe"

def do_file(action, file_path, options):
    """ Do the specified action(s) on the given file. """
    verbose = options.get("verbose", False)
    metadata = fo.fits_metadata(file_path, options)
    ihelper = ih.IrodsHelper(options=options)
    ensure_astrolabe_root(ihelper, options)
    ihelper.put_file(file_path)
    ihelper.put_metaf(file_path, metadata)
    return True


def do_tree(action, root_path, options):
    """ Walk the filesystem tree from the given root_node and do the specified action(s)
        on the files and directories.
    """
    # action_setup(action, images_path, options)
    for fits_file in filter_file_tree(images_path):
        # TODO: IMPLEMENT LATER
        pass
    # action_dispatch(action, fits_file, options)
    # action_cleanup(action, images_path, options)


def filter_file_tree(root_dir):
    """ Generator to yield all FITS files in the file tree under the given root directory. """
    fits_pat = "*.fits"                     # pattern for identifying FITS files
    gzfits_pat = "*.fits.gz"                # pattern for identifying gzipped FITS files
    for root, dirs, files in os.walk(root_dir):
        for fyl in files:
            if (fnmatch.fnmatch(fyl, fits_pat) or fnmatch.fnmatch(fyl, gzfits_pat)):
                file_path = os.path.join(root, fyl)
                yield file_path

def ensure_astrolabe_root(ihelper, options):
    """ Ensure that the Astrolabe root directory exists and set it as the user's root directory. """
    ihelper.set_root()                      # reset root to user iRod root dir
    ihelper.cd_root()                       # set cwd to user iRod root dir
    ihelper.mkdir(_ASTROLABE_ROOT_DIR)      # make the Astrolabe directory
    ihelper.set_root(top_dir=_ASTROLABE_ROOT_DIR) # reset root to Astrolabe dir
