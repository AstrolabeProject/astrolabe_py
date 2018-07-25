#
# Test context file: obviate need to install module before testing.
#   Written by: Tom Hicks. 6/30/2018.
#   Last Modified: Add uploader import.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import astrolabe_uploader.fits_meta as fm
import astrolabe_uploader.fits_ops as fo
import astrolabe_uploader.irods_help as ih
import astrolabe_uploader.uploader as up
# import astrolabe_uploader.wwt_help as wh
