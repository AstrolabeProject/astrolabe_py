#!/usr/bin/env python3
#
# Program to view, extract, and/or verify metadata from one or more FITS files.
#   Written by: Tom Hicks. 7/18/2018.
#   Last Modified: Move this module up. Switch to argparse.
#
import argparse
import os
import sys

from astrolabe_uploader import __version__
import astrolabe_uploader.uploader as up

# Text file of desired metadata keys, one per line
_DEFAULT_KEYS_FILE = "metadata-keys.txt"

def get_metadata_keys(options):
    """ Return a list of metadata keys to be extracted. """
    keyfile = options.get("keyfile")
    with open(keyfile, "r") as mdkeys_file:
        return mdkeys_file.read().splitlines()


def main(argv):
    """ Perform actions on a FITS file or a directory of FITS files. """
    options = { "action": "md" }
    is_file = False                         # assume directory by default
    program = "ALUP"
    version = "{} version {}".format(program, __version__)

    parser = argparse.ArgumentParser(
        prog=program,
        allow_abbrev=False,
        description="Perform actions on a FITS file or a directory of FITS files."
    )
    parser.add_argument("-a", "--action",
                        choices=["check", "info", "store"],
                        default="store",
                        help="action to perform on FITS file(s)")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="provide more information during execution")

    parser.add_argument("-u", "--upload-only", action="store_true",
                        help="upload files to iRods only: do not process file metadata")

    parser.add_argument("--version", action="version", version=version)

    parser.add_argument("--keyfile", nargs="?", const="metadata-keys.txt",
                        metavar="metadata-keyfile",
                        help="a file specifying which metadata keys which should be processed")

    parser.add_argument("images_path",
                        help="path to FITS file or directory of FITS files")

    args = vars(parser.parse_args(argv))    # parse arguments into a dictionary
    # print("ARGS={}".format(args))           # DEBUGGING

    # check the keyfile path argument, if given
    keyfile = args.get("keyfile")
    if (keyfile and ((len(keyfile) < 1) or (not os.path.isfile(keyfile)))):
        print("Error: --keyfile argument must specify the path to a readable key file")
        parser.print_usage()
        sys.exit(4)

    # check the image file or directory path argument, if given
    # if ((len(args) < 1) or (not args[0].strip())):
    #     print("Error: Missing required argument: path to image file or images directory")
    #     print(usage)
    #     sys.exit(3)

    # insure that the given path refers to a readable file or valid directory
    images_path = args.get("images_path")
    if (not os.path.exists(images_path)):   # alread insure non-empty by argparse
        print("Error: Specified images path '{}' not found or is not readable".format(images_path))
        sys.exit(5)

    if (not os.access(images_path, os.R_OK)):
        print("Error: Specified images path '{}' is not readable".format(images_path))
        sys.exit(6)

    # figure out the action to perform on the files
    action = args.get("action", "store")

    # # execute action sequence for a single file or a directory of files
    # if (os.path.isfile(images_path)):
    #     up.do_file(action, images_path, options)
    # else:
    #     if (os.path.isdir(images_path)):
    #         up.do_tree(action, images_path, options)
    #     else:
    #         print("Error: Specified images path '{}' is not a file or directory".format(images_path))
    #         sys.exit(7)


if __name__ == "__main__":
    main(sys.argv[1:])
