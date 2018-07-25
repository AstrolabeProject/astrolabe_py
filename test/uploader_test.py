#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Operations module.
#   Written by: Tom Hicks. 7/25/2018.
#   Last Modified: Initial creation of infrastructure stub.
#
import unittest
from astropy.io import fits

from context import up                      # the module under test

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FileTestCase))
  return suite


class ULTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = { "verbose": True }
    cls.test_file = "cvnidwabcut.fits"


class FileTestCase(ULTestCase):

  def setUp(self):
    "Initialize the test case"
    self.hduList = fits.open(self.test_file)

  def tearDown(self):
    self.hduList.close()

  def test_stub(self):
    print("\nHDU List of file {} is {}".format(self.test_file, self.hduList))


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
