#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Operations module.
#   Written by: Tom Hicks. 7/25/2018.
#   Last Modified: Add tests for paths containing dots.
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
    cls.default_options = { }
    cls.root_dir = up._ASTROLABE_ROOT_DIR
    cls.test_dir = "resources"
    cls.test_dir_fits_count = 4
    cls.empty_dir = "resources/empty_dir"
    cls.empty2_dir = "resources/test2"
    cls.test_fileB = "resources/cvnidwabcut.fits"
    cls.test_fileB_md_count = 64             # added 62 to initial 2 metadata items
    cls.test_file = "resources/m13.fits"
    cls.test_file_md_count = 25             # added 23 to initial 2 metadata items
    cls.test_md_keysfile = "md-keys-subset.txt"
    cls.test_md_keycount = 12               # test fileB only has 12 relevant keys
    cls.ignored_keys = set(["COMMENT", "HISTORY"])


class FileTestCase(ULTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = ih.IrodsHelper()
    self.assertTrue(self.ihelper.is_connected())

  def tearDown(self):
    self.ihelper.disconnect()


  def test_execute_dot1(self):
    "Throws exception on image path of a single dot"
    with self.assertRaises(SystemExit):
      options = { "images_path": ".", "verbose": True }
      up.execute(options)

  def test_execute_dots2(self):
    "Throws exception on image path of a double dot"
    with self.assertRaises(SystemExit):
      options = { "images_path": "..", "verbose": True }
      up.execute(options)

  def test_execute_dots2_leading(self):
    "Throws exception on image path with double leading dots"
    with self.assertRaises(SystemExit):
      options = { "images_path": "../resources", "verbose": True }
      up.execute(options)

  def test_execute_2dots_inner(self):
    "Throws exception on image path with embedded double dots"
    with self.assertRaises(SystemExit):
      options = { "images_path": "resources/../test2", "verbose": True }
      up.execute(options)

  def test_execute_dots2_trailing(self):
    "Throws exception on image path with trailing double dots"
    with self.assertRaises(SystemExit):
      options = { "images_path": "resources/test2/..", "verbose": True }
      up.execute(options)

  def test_execute_dots_mixed(self):
    "Throws exception on image path with mixed single and double dots"
    with self.assertRaises(SystemExit):
      options = { "images_path": "./..", "verbose": True }
      up.execute(options)


  def test_execute_dir_empty(self):
    "Processing directory with no files does nothing"
    print()
    options = { "images_path": self.empty_dir, "verbose": True }
    rets = up.execute(options)
    self.assertNotEqual(rets, None)
    self.assertEqual(len(rets), 0)

  def test_execute_dir_nofits(self):
    "Processing directory with no FITS files does nothing"
    print()
    options = { "images_path": self.empty2_dir, "verbose": True }
    rets = up.execute(options)
    self.assertNotEqual(rets, None)
    self.assertEqual(len(rets), 0)

  def test_execute_dir(self):
    "Process a directory with several FITS files at once"
    print()
    options = { "images_path": self.test_dir, "verbose": True }
    rets = up.execute(options)
    self.assertNotEqual(rets, None)
    self.assertEqual(len(rets), self.test_dir_fits_count)
    self.assertTrue(all(rets))

  def test_execute_file1(self):
    "Process a single FITS file to the astrolabe directory"
    print()
    upfile = self.test_file
    basefile = os.path.basename(upfile)
    options = { "images_path": upfile, "verbose": True, "ignore_keys": self.ignored_keys }
    rets = up.execute(options)              # the test call
    self.assertNotEqual(rets, None)
    self.assertEqual(len(rets), 1)
    self.assertTrue(all(rets))
    # now fetch and test the metadata just created:
    md = self.ihelper.get_metaf("{}/{}".format(self.root_dir, basefile))
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertEqual(len(md), self.test_file_md_count)

  def test_execute_file1_mdsubset(self):
    "Process a single FITS file to the astrolabe directory with reduced metadata keyset"
    print()
    upfile = self.test_fileB
    basefile = os.path.basename(upfile)
    options = { "images_path": upfile, "verbose": True,
                "keyfile": self.test_md_keysfile, "ignore_keys": self.ignored_keys }
    rets = up.execute(options)              # the test call
    self.assertNotEqual(rets, None)
    self.assertEqual(len(rets), 1)
    self.assertTrue(all(rets))
    # now fetch and test the metadata just created:
    md = self.ihelper.get_metaf("{}/{}".format(self.root_dir, basefile))
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertEqual(len(md), self.test_md_keycount)

  def test_execute_file1_rename(self):
    "Process a single FITS file to the astrolabe directory with rename"
    print()
    upfile = self.test_file
    newname = "m13_copy2.fits"
    options = { "images_path": upfile, "to_path": newname, "verbose": True,
                "ignore_keys": self.ignored_keys }
    rets = up.execute(options)              # the test call
    self.assertNotEqual(rets, None)
    self.assertEqual(len(rets), 1)
    self.assertTrue(all(rets))
    # now fetch and test the metadata just created:
    md = self.ihelper.get_metaf("{}/{}".format(self.root_dir, newname))
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertEqual(len(md), self.test_file_md_count)


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
