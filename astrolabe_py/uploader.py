#
# Module to extract metadata and upload one or more FITS files to iRods.
#   Written by: Tom Hicks. 7/19/2018.
#   Last Modified: Maintain return of same truth vector as previous version.
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
        print("Error: Images path argument must be asbolute; it may not contain '..' or '.'")
        sys.exit(10)

    if (os.path.isfile(images_path)):
        to_path = options.get("to_path")    # allow for future expansion
        if (not to_path):
            to_path = os.path.basename(images_path)
        return [ do_file(ihelper, images_path, to_path, options) ]
    else:
        if (os.path.isdir(images_path)):
            return do_tree(ihelper, images_path, options)
        else:
            print("Error: Specified images path '{}' is not a file or directory".format(images_path))
            sys.exit(11)


def do_file(ihelper, source_file, to_path, options):
    """ Do metadata extraction, file upload, and metadata attachment for the given file,
        depending on the settings of the various arguments in the given 'options' dictionary.
    """
    verbose = options.get("verbose", False)
    upload_only = options.get("upload_only", False)

    if (verbose):
        print("Uploading file {} to {}".format(source_file, to_path))
    ihelper.put_file(source_file, to_path, absolute=True)

    if ((not upload_only) and has_metadata(source_file)):
        if (verbose):
            print("Extracting metadata from file {}".format(source_file))
        metadata = fo.fits_metadata(source_file, options)
        if (verbose):
            print("Attaching metadata to file {}".format(to_path))
        ihelper.put_metaf(metadata, to_path)

    return True


def do_tree(ihelper, root_node, options):
    """ Walk the local filesystem tree from the given root_node and process any FITS files.
        The walk creates a parallel tree in the iRods Astrolabe area and calls do_file to
        upload the files (and possibly their metadata) to the corresponding iRods directories.
    """
    root_path = os.path.normpath(root_node) # remove any trailing slashes from given root path

    # get a list of files to be uploaded
    source_paths = get_source_paths(root_path, options)

    # remove the root path prefix from the upload files
    suffix_paths = make_suffix_paths(root_path, source_paths, options)

    # make a list of directories to be created in iRods and create them
    dir_paths = make_dir_paths(suffix_paths, options)
    for adir in dir_paths:
        ihelper.mkdir(adir, absolute=True)  # make corresponding iRods directory

    # make a list of user-home-relative target file paths
    target_paths = make_target_paths(suffix_paths, options)

    # pair up the local source file paths and the iRods target file paths, then upload the files
    return [ do_file(ihelper, pair[0], pair[1], options) for pair in zip(source_paths, target_paths) ]


def ensure_astrolabe_root(ihelper):
    """ Ensure that the Astrolabe root directory exists and set it as the user's root directory. """
    ihelper.set_root()                      # reset root to user iRod root dir
    ihelper.cd_root()                       # set cwd to user iRod root dir
    ihelper.mkdir(_ASTROLABE_ROOT_DIR)      # make the Astrolabe directory
    ihelper.set_root(top_dir=_ASTROLABE_ROOT_DIR) # reset root to Astrolabe dir


def get_source_paths(root_path, options):
    """Walk the given root path, returning a list of paths for files to be uploaded."""
    results = []
    for root, dirs, files in os.walk(root_path):
        for afile in files:                 # for files at this level
            if (isa_desired_file(afile)):   # if a file is to be uploaded
                results.append(os.path.join(root, afile)) # local source path
    return results


def has_metadata(afile):
    """Return true if the given file is one that contains metadata. Currently, only FITS files."""
    return (utils.is_fits_file(afile))      # if a file is a FITS file

def isa_desired_file(afile):
    """Return true if the given file is one that is to be uploaded. Currently, only FITS files."""
    return (utils.is_fits_file(afile))      # if a file is a FITS file


def make_dir_paths(file_paths, options):
    """Return a sorted list of unique directory paths, extracted from the given list
       of file paths.
    """
    return sorted({os.path.split(path)[0] for path in file_paths}, reverse=True)


def make_suffix_paths(root_path, source_paths, options):
    """Remove the given root path from each of the paths in the given source path list."""
    source_prefix = os.path.split(root_path)[0] # find local path prefix preceding root node
    # print("PREFIX: {}".format(source_prefix))
    return [os.path.relpath(path, source_prefix) for path in source_paths]


def make_target_paths(suffix_paths, options, irods_prefix=_ASTROLABE_ROOT_DIR):
    """Return a list of user-home-relative iRods paths for the given list of local file paths."""
    return suffix_paths                     # currently a NOP
    # return [os.path.join(irods_prefix, afile) for afile in suffix_paths]
