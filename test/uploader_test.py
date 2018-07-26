#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Operations module.
#   Written by: Tom Hicks. 7/25/2018.
#   Last Modified: Add first do_file test.
#
import unittest
from astropy.io import fits

from context import fm
from context import ih
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
    cls.root_dir = up._ASTROLABE_ROOT_DIR
    cls.test_file = "cvnidwabcut.fits"
    cls.test_file_md_count = 64             # added 62 to initial 2 metadata items


class FileTestCase(ULTestCase):

  def setUp(self):
    "Initialize the test case"
    pass

  def tearDown(self):
    pass

  def test_do_file(self):
    filename = self.test_file
    filepath = "{}/{}".format(self.root_dir, filename)
    ret = up.do_file("XNUP", filename, self.default_options) # the test call
    self.assertTrue(ret)

    helper = ih.IrodsHelper()
    md = helper.get_metaf(filepath)
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)
    self.assertEqual(len(md), self.test_file_md_count)


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
