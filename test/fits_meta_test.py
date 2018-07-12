#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Metadata module.
#   Written by: Tom Hicks. 7/11/2018.
#   Last Modified: Add tests for __contains__, __iter__, and key_set methods.
#
import unittest

from context import fm                      # the module under test

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FitsMetaTestCase))
  return suite


class FitsMetaBaseTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.test_files = [ "cvnidwabcut.fits" ]


class FitsMetaTestCase(FitsMetaBaseTestCase):

  def setUp(self):
    "Initialize the test case"
    self.fm = fm.FitsMeta(self.test_files[0])

  def tearDown(self):
    "Cleanup after the test case"
    pass


  def test_bad_ctor_filename(self):
    "Throws exception on bad FITS filename"
    with self.assertRaises(FileNotFoundError):
      fm.FitsMeta("BAD_FILENAME")

  def test_filename(self):
    "Get filename of test file"
    self.assertEqual(self.fm.filename(), self.test_files[0])

  def test_len(self):
    "Get length of metadata from real data"
    self.assertEqual(len(self.fm), 54)

  def test_metadata(self):
    "Get metadata from real data"
    md = self.fm.metadata()
    self.assertNotEqual(md, None)
    self.assertEqual(len(md), 54)
    # [print(item) for item in md]

  def test_key_set(self):
    "Get the set of metadata keywords (from real data)"
    keys = self.fm.key_set()
    self.assertNotEqual(keys, None)
    self.assertEqual(len(keys), 53)         # HISTORY keyword is repeated in test file
    # [print(k) for k in keys]

  def test_contains(self):
    "Test membership in the set of metadata keywords (from real data)"
    self.assertFalse("" in self.fm)
    self.assertFalse(None in self.fm)
    self.assertFalse("XXX" in self.fm)
    self.assertTrue("NAXIS" in self.fm)
    self.assertTrue("HISTORY" in self.fm)

  def test_iteration(self):
    "Get an iterator over the metadata class"
    md = [item for item in self.fm]
    self.assertNotEqual(md, None)
    self.assertEqual(len(md), 54)
    self.assertEqual(md, self.fm.metadata())


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
