#!/usr/bin/env python3
#
# Program to view, extract, and/or verify metadata from one or more FITS files.
#   Written by: Tom Hicks. 7/18/2018.
#   Last Modified: Move file filter to uploader.
#
import getopt
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    options = { "action": "info" }
    is_file = False                         # assume directory by default
    usage = "Usage: fits.py [-h|--help] [--info|--metadata|--verify] [--keyfile metadata-keyfile] images_path"

    # parse the command line arguments:
    try:
        opts, args = getopt.getopt(argv,"himvk",["help", "info", "metadata", "verify", "keyfile="])
    except getopt.GetoptError as err:
        print(err)
        print(usage)
        sys.exit(-1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usage)
            sys.exit(1)
        elif opt in ("--info"):
            options["action"] = "info"
        elif opt in ("--metadata"):
            options["action"] = "metadata"
        elif opt in ("--verify"):
            options["action"] = "verify"
        elif opt in ("--keyfile"):
            options["keyfile"] = arg.strip()
        else:
            print("Error: Unrecognized command line option")
            print(usage)
            sys.exit(2)

    # check the keyfile path argument, if given
    keyfile = options.get("keyfile")
    if (keyfile and ((len(keyfile) < 1) or (not os.path.isfile(keyfile)))):
        print("Error: --keyfile argument must specify the path to a readable key file")
        print(usage)
        sys.exit(4)

    # check the image file or directory path argument, if given
    if ((len(args) < 1) or (not args[0].strip())):
        print("Error: Missing required argument: path to image file or images directory")
        print(usage)
        sys.exit(3)

    # insure that the given path refers to a readable file or valid directory
    images_path = args[0].strip()                   # already insured non-empty above
    if (not os.path.exists(images_path)):
        print("Error: Specified images path '{}' not found or is not readable".format(images_path))
        sys.exit(5)

    if (not os.access(images_path, os.R_OK)):
        print("Error: Specified images path '{}' is not readable".format(images_path))
        sys.exit(6)

    # figure out the action to perform on the files
    action = options.get("action", "info")

    # execute action sequence for a single file or a directory of files
    if (os.path.isfile(images_path)):
        up.do_file(action, images_path, options)
    else:
        if (os.path.isdir(images_path)):
            up.do_tree(action, images_path, options)
        else:
            print("Error: Specified images path '{}' is not a file or directory".format(images_path))
            sys.exit(7)


if __name__ == "__main__":
    main(sys.argv[1:])
