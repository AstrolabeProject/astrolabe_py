#!/usr/bin/env python3
#
# Python code to unit test reading FITS files from iRods.
#   Written by: Tom Hicks. 12/30/2018.
#   Last Modified: Initial creation.
#
import os
import unittest
from irods.session import iRODSSession
from irods.exception import CollectionDoesNotExist, DataObjectDoesNotExist

from context import ih                      # the module under test
from context import up
from astrolabe_py import Metadatum

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ReadTestCase))
  return suite


class IrodsHelpTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = { "irods_env_file": "irods_env_file.json" }
    cls.irods_env_file = "irods_env_file.json"
    cls.root_dir = up._ASTROLABE_ROOT_DIR


class ReadTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = ih.IrodsHelper()          # create instance of class under test
    self.assertTrue(self.ihelper.is_connected())

  def tearDown(self):
    "Cleanup the test case"
    self.ihelper.disconnect()

  def test_read(self):
    "Return a File Object for a known test file"
    afile = "sample-data/w5/w5.fits"
    obj = self.ihelper.getf(afile)          # get a known test file
    self.assertNotEqual(obj, None)
    filename = os.path.basename(afile)
    self.assertEqual(obj.name, filename)
    with obj.open('r+') as infyl, open("/tmp/w5-copy.fits", "wb") as outfyl:
      print("\nreading {}...".format(afile))
      contents = infyl.read()
      print("writing {}...".format(outfyl.name))
      outfyl.write(contents)


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
