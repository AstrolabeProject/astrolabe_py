#
# Test context file: obviate need to install module before testing.
#   Written by: Tom Hicks. 6/30/2018.
#   Last Modified: Update for project rename.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import astrolabe_py.fits_meta as fm
import astrolabe_py.fits_ops as fo
import astrolabe_py.irods_help as ih
import astrolabe_py.uploader as up
# import astrolabe_py.wwt_help as wh
