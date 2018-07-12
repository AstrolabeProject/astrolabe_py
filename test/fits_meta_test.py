#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Metadata module.
#   Written by: Tom Hicks. 7/11/2018.
#   Last Modified: Add bad filename test. Update for accessor methods and metadata cleanup.
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

  def test_fm_filename(self):
    "Get filename of test file"
    self.assertEqual(self.fm.filename(), self.test_files[0])

  def test_fm_len(self):
    "Get length of metadata from real data"
    self.assertEqual(len(self.fm), 54)

  def test_fm_metadata(self):
    "Get metadata from real data"
    md = self.fm.metadata()
    self.assertNotEqual(md, None)
    self.assertEqual(len(md), 54)


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
