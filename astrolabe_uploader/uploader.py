#
# Module to extract metadata and upload one or more FITS files to iRods.
#   Written by: Tom Hicks. 7/19/2018.
#   Last Modified: Implement working versions of execute, do_file, and do_tree.
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
        return [ do_file(ihelper, images_path, options) ]
    else:
        if (os.path.isdir(images_path)):
            return do_tree(ihelper, images_path, options)
        else:
            print("Error: Specified images path '{}' is not a file or directory".format(images_path))
            sys.exit(10)


def do_file(ihelper, local_file, options):
    """ Do metadata extraction, file upload, and metadata attachment for the given file,
        depending on the settings of the various arguments in the given 'options' dictionary.
    """
    verbose = options.get("verbose", False)
    upload_only = options.get("upload-only", False)

    to_path = options.get("to_path")
    if (not to_path):
        to_path = os.path.basename(local_file)

    if (verbose):
        print("Uploading file {} to {} ...".format(local_file, to_path))
    ihelper.put_file(local_file, to_path)

    if (not upload_only):
        if (verbose):
            print("Extracting metadata from file {} ...".format(local_file))
        metadata = fo.fits_metadata(local_file, options)
        if (verbose):
            print("Attaching metadata to file {} ...".format(to_path))
        ihelper.put_metaf(metadata, to_path)

    return True


def do_tree(ihelper, root_path, options):
    """ Walk the filesystem tree from the given root_node and process the FITS files in it. """
    results = []
    for fits_file in utils.filter_file_tree(root_path):
        results.append(do_file(ihelper, fits_file, options))
    return results


def ensure_astrolabe_root(ihelper):
    """ Ensure that the Astrolabe root directory exists and set it as the user's root directory. """
    ihelper.set_root()                      # reset root to user iRod root dir
    ihelper.cd_root()                       # set cwd to user iRod root dir
    ihelper.mkdir(_ASTROLABE_ROOT_DIR)      # make the Astrolabe directory
    ihelper.set_root(top_dir=_ASTROLABE_ROOT_DIR) # reset root to Astrolabe dir
