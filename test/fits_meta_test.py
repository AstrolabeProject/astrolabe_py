#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Metadata module.
#   Written by: Tom Hicks. 7/11/2018.
#   Last Modified: Add tests for default_cleaner_fn and JSON metadata. Update for renames to filepath.
#
import json
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
    cls.test_file = "cvnidwabcut.fits"
    cls.test_file_md_count = 55


class FitsMetaTestCase(FitsMetaBaseTestCase):

  def setUp(self):
    "Initialize the test case"
    self.fm = fm.FitsMeta(self.test_file)

  def tearDown(self):
    "Cleanup after the test case"
    pass


  def test_bad_ctor_filepath(self):
    "Throws exception on bad FITS filepath"
    with self.assertRaises(FileNotFoundError):
      fm.FitsMeta("BAD_FILENAME")

  def test_filepath(self):
    "Get filepath of test file"
    self.assertEqual(self.fm.filepath(), self.test_file)

  def test_len(self):
    "Get length of metadata from real data"
    self.assertEqual(len(self.fm), self.test_file_md_count)

  def test_metadata(self):
    "Get metadata from real data"
    md = self.fm.metadata()
    self.assertNotEqual(md, None)
    self.assertEqual(len(md), self.test_file_md_count)
    # [print(item) for item in md]

  def test_key_set(self):
    "Get the set of metadata keywords (from real data)"
    keys = self.fm.key_set()
    self.assertNotEqual(keys, None)
    # HISTORY keyword is repeated in test file:
    self.assertEqual(len(keys), self.test_file_md_count - 1)
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
    self.assertEqual(len(md), self.test_file_md_count)
    self.assertEqual(md, self.fm.metadata())

  def test_metadata_json(self):
    "Get metadata as JSON from real data"
    jmd = self.fm.metadata_json()
    self.assertNotEqual(jmd, None)
    self.assertEqual(type(jmd), str)
    json_data = json.loads(jmd)
    self.assertEqual(type(json_data), list)
    self.assertEqual(type(json_data), list)
    self.assertEqual(len(json_data), self.test_file_md_count)
    self.assertTrue(all([type(j) == list for j in json_data]))
    self.assertTrue(all([len(j) == 2 for j in json_data]))

  def test_default_cleaner(self):
    "The default cleaner function removes single quotes, double quotes, and backslashes"
    dirty = [ "\'B M\' E\'", "'B M' E'", '\"B M\" E\"', '"B M" E"', "\\B M\\ E\\", "\B M\ E\"" ]
    clean = [fm.default_cleaner_fn(v) for v in dirty]
    self.assertNotEqual(clean, None)
    self.assertTrue(all([v == "B M E" for v in clean]))


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
