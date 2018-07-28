#
# Module to extract metadata and upload one or more FITS files to iRods.
#   Written by: Tom Hicks. 7/19/2018.
#   Last Modified: Add top-level execute method. Continue building do_file. Stub do_tree.
#
import os
import sys
import logging
import fnmatch

import astrolabe_uploader.fits_ops as fo
import astrolabe_uploader.irods_help as ih
import astrolabe_uploader.utils as utils

logging.basicConfig(level=logging.INFO)     # default logging configuration

_ASTROLABE_ROOT_DIR = "astrolabe"

def execute(options):
    """ Process the specified file(s) according to the other given arguments.
        This module operates on one or more FITS files to extract metadata,
        uploads the files to iRods, and attach the metadata to the files.
    """
    # create connection to iRods
    ihelper = ih.IrodsHelper()
    if (not ihelper.is_connected()):
        pass                                # TODO: handle this case
    ensure_astrolabe_root(ihelper)          # create/use astrolabe directory, as needed

    # TODO: load keysfile, if specified

    # execute action for a single file or a directory of files
    images_path = options.get("images_path")
    if (os.path.isfile(images_path)):
        do_file(ihelper, images_path, options)
    else:
        if (os.path.isdir(images_path)):
            up.do_tree(ihelper, images_path, options)
        else:
            print("Error: Specified images path '{}' is not a file or directory".format(images_path))
            sys.exit(10)


def do_file(ihelper, local_file, to_path, options):
    """ Do metadata extraction, file upload, and metadata attachment for the given file,
        locating it at the given 'to_path'.
    """
    verbose = options.get("verbose", False)
    upload_only = options.get("upload-only", False)

    ihelper.put_file(local_file, to_path)
    if (not upload_only):
        metadata = fo.fits_metadata(local_file, options)
        ihelper.put_metaf(metadata, to_path)
    return True


def do_tree(ihelper, root_path, options):
    """ Walk the filesystem tree from the given root_node and do the specified action(s)
        on the files and directories.
    """
    # action_setup(action, root_path, options)
    print()                                 # REMOVE LATER
    for fits_file in utils.filter_file_tree(root_path):
        # TODO: IMPLEMENT LATER
        print("uploader: processing file {}".format(fits_file)) # REMOVE LATER
    # action_dispatch(action, fits_file, options)
    # action_cleanup(action, root_path, options)
    return True


def ensure_astrolabe_root(ihelper):
    """ Ensure that the Astrolabe root directory exists and set it as the user's root directory. """
    ihelper.set_root()                      # reset root to user iRod root dir
    ihelper.cd_root()                       # set cwd to user iRod root dir
    ihelper.mkdir(_ASTROLABE_ROOT_DIR)      # make the Astrolabe directory
    ihelper.set_root(top_dir=_ASTROLABE_ROOT_DIR) # reset root to Astrolabe dir
