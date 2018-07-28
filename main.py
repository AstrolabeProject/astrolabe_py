#!/usr/bin/env python3
#
# Program to view, extract, and/or verify metadata from one or more FITS files.
#   Written by: Tom Hicks. 7/18/2018.
#   Last Modified: Add action dispatch to other modules.
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
                        help="path to a FITS file or a directory of FITS files to be processed")

    args = vars(parser.parse_args(argv))    # parse arguments into a dictionary
    # print("ARGS={}".format(args))           # DEBUGGING

    # check the keyfile path argument, if given
    keyfile = args.get("keyfile")
    if (keyfile and ((len(keyfile) < 1) or (not os.path.isfile(keyfile)))):
        print("Error: --keyfile argument must specify the path to a readable key file")
        parser.print_usage()
        sys.exit(4)

    # insure that the given path refers to a readable file or valid directory
    images_path = args.get("images_path")
    if (not os.path.exists(images_path)):   # alread insure non-empty by argparse
        print("Error: Specified images path '{}' not found or is not readable".format(images_path))
        sys.exit(5)

    if (not os.access(images_path, os.R_OK)):
        print("Error: Specified images path '{}' is not readable".format(images_path))
        sys.exit(6)

    # figure out the action to perform on the files; default to extract & upload:
    action = args.get("action", "store")
    if (action == "store"):                 # upload and/or attach metadata
        up.execute(args)
    elif (action == "check"):               # check files for problems
        pass
    elif (action == "info"):                # produce HDU info for the files
        pass
    else:
        print("Error: Action '{}' is not implemented. Please specify a valid action".format(action))
        parser.print_usage()
        sys.exit(7)


if __name__ == "__main__":
    main(sys.argv[1:])
