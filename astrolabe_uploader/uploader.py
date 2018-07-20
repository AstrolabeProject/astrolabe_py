#
# Module to extract metadata and upload one or more FITS files to iRods.
#   Written by: Tom Hicks. 7/19/2018.
#   Last Modified: WIP: Initial creation.
#
import os
import sys
import logging

import astrolabe_uploader.fits_ops as fo
import astrolabe_uploader.irods_help as ih

logging.basicConfig(level=logging.INFO)     # default logging configuration

_ASTROLABE_ROOT_DIR = "astrolabe"

def do_file(action, file_path, options):
    """ Do the specified action(s) on the given file. """
    verbose = options.get("verbose", False)
    metadata = fo.fits_metadata(file_path, options)
    logging.info("Extracted {} metadata items from {}".format(len(metadata), file_path))
    ihelper = ih.IrodsHelper()
    ihelper.connect(options)
    ensure_astrolabe_root(ihelper, options)
    ihelper.put(file_path)


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


def ensure_astrolabe_root(ihelper, options):
    """ Ensure that the Astrolabe root directory exists and set it as the user's root directory. """
    ihelper.set_root()                      # reset root to user iRod root dir
    ihelper.cd_root()                       # set cwd to user iRod root dir
    ihelper.mkdir(_ASTROLABE_ROOT_DIR)      # make the Astrolabe directory
    ihelper.set_root(top_dir=_ASTROLABE_ROOT_DIR) # reset root to Astrolabe dir
