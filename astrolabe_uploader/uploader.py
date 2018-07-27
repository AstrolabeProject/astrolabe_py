#
# Module to extract metadata and upload one or more FITS files to iRods.
#   Written by: Tom Hicks. 7/19/2018.
#   Last Modified: Refactor filter to utils module. Implement rudimentary do_file.
#
import os
import sys
import logging
import fnmatch

import astrolabe_uploader.fits_ops as fo
import astrolabe_uploader.irods_help as ih
import astrolabe_uploader.utils

logging.basicConfig(level=logging.INFO)     # default logging configuration

_ASTROLABE_ROOT_DIR = "astrolabe"

def do_file(ihelper, local_file, to_path, options={}):
    """ Do metadata extraction, file upload, and metadata attachment for the given file,
        locating it at the given 'to_path'.
    """
    verbose = options.get("verbose", False)
    ihelper.put_file(local_file, to_path)
    metadata = fo.fits_metadata(local_file, options)
    ihelper.put_metaf(metadata, to_path)
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


def ensure_astrolabe_root(ihelper):
    """ Ensure that the Astrolabe root directory exists and set it as the user's root directory. """
    ihelper.set_root()                      # reset root to user iRod root dir
    ihelper.cd_root()                       # set cwd to user iRod root dir
    ihelper.mkdir(_ASTROLABE_ROOT_DIR)      # make the Astrolabe directory
    ihelper.set_root(top_dir=_ASTROLABE_ROOT_DIR) # reset root to Astrolabe dir
