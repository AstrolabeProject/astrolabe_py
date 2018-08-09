#
# Module to extract metadata and upload one or more FITS files to iRods.
#   Written by: Tom Hicks. 7/19/2018.
#   Last Modified: Check for and exclude dots paths.
#
import os
import sys
import logging
import fnmatch

import astrolabe_py.fits_ops as fo
import astrolabe_py.irods_help as ih
import astrolabe_py.utils as utils

logging.basicConfig(level=logging.INFO)     # default logging configuration

_ASTROLABE_ROOT_DIR = "astrolabe"

def execute(options):
    """ Process the specified file(s) according to the other given arguments.
        This module operates on one or more FITS files to extract metadata,
        uploads the files to iRods, and attach the metadata to the files.
    """
    # create connection to iRods
    ihelper = ih.IrodsHelper()
    ensure_astrolabe_root(ihelper)          # create/use astrolabe directory, as needed

    # get the desired subset of metadata keys, if any specified by a keyfile
    md_keys = utils.get_metadata_keys(options)
    if (md_keys):
        options["keys_subset"] = md_keys

    # execute action for a single file or a directory of files
    images_path = options.get("images_path")
    if (utils.path_has_dots(images_path)):
        print("Error: Images path argument may not contain '..' or '.'")
        sys.exit(10)

    if (os.path.isfile(images_path)):
        return [ do_file(ihelper, images_path, options) ]
    else:
        if (os.path.isdir(images_path)):
            return do_tree(ihelper, images_path, options)
        else:
            print("Error: Specified images path '{}' is not a file or directory".format(images_path))
            sys.exit(11)


def do_file(ihelper, local_file, options):
    """ Do metadata extraction, file upload, and metadata attachment for the given file,
        depending on the settings of the various arguments in the given 'options' dictionary.
    """
    verbose = options.get("verbose", False)
    upload_only = options.get("upload_only", False)

    to_path = options.get("to_path")
    if (not to_path):
        to_path = os.path.basename(local_file)

    if (verbose):
        print("Uploading file {} to {}".format(local_file, to_path))
    ihelper.put_file(local_file, to_path)

    if (not upload_only):
        if (verbose):
            print("Extracting metadata from file {}".format(local_file))
        metadata = fo.fits_metadata(local_file, options)
        if (verbose):
            print("Attaching metadata to file {}".format(to_path))
        ihelper.put_metaf(metadata, to_path)

    return True


def do_tree(ihelper, root_path, options):
    """ Walk the local filesystem tree from the given root_node and process any FITS files.
        The walk creates a parallel tree in the iRods Astrolabe area and calls do_file to
        upload the files (and possibly their metadata) to the corresponding iRods directories.
    """
    results = []
    for root, dirs, files in os.walk(root_path):
        ihelper.mkdir(root, absolute=True)  # make corresponding iRods directory
        ihelper.cd(root, absolute=True)     # make it the current working directory
        for afile in files:                 # for files at this level
            if (utils.is_fits_file(afile)): # if a file is a FITS file
                local_filepath = os.path.join(root, afile)
                results.append(do_file(ihelper, local_filepath, options))
    return results


def ensure_astrolabe_root(ihelper):
    """ Ensure that the Astrolabe root directory exists and set it as the user's root directory. """
    ihelper.set_root()                      # reset root to user iRod root dir
    ihelper.cd_root()                       # set cwd to user iRod root dir
    ihelper.mkdir(_ASTROLABE_ROOT_DIR)      # make the Astrolabe directory
    ihelper.set_root(top_dir=_ASTROLABE_ROOT_DIR) # reset root to Astrolabe dir
