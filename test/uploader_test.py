#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Operations module.
#   Written by: Tom Hicks. 7/25/2018.
#   Last Modified: Add basic do_tree test.
#
import os
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
    # cls.test_file = "resources/cvnidwabcut.fits"
    # cls.test_file_md_count = 64             # added 62 to initial 2 metadata items
    cls.test_file = "resources/m13.fits"
    cls.test_file_md_count = 25             # added 23 to initial 2 metadata items
    cls.test_dir = "resources"


class FileTestCase(ULTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = ih.IrodsHelper()
    self.assertTrue(self.ihelper.is_connected())
    up.ensure_astrolabe_root(self.ihelper)  # create/use astrolabe directory

  def tearDown(self):
    self.ihelper.disconnect()


  def test_do_file(self):
    """ Process and upload a single test file. """
    upfile = self.test_file
    basefile = os.path.basename(upfile)
    ret = up.do_file(self.ihelper, upfile, basefile, options=self.default_options)
    self.assertTrue(ret)

    md = self.ihelper.get_metaf(basefile)
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)
    self.assertEqual(len(md), self.test_file_md_count)


  def test_do_tree_basic(self):
    """ Process and upload files from a directory. """
    updir = self.test_dir
    ret = up.do_tree(self.ihelper, updir, options=self.default_options)
    self.assertTrue(ret)
    # TODO: walk both trees in parallel and compare


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
