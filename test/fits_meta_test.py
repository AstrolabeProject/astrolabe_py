#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Metadata module.
#   Written by: Tom Hicks. 7/11/2018.
#   Last Modified: Add tests for get and __getitem__.
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
    "Get length of metadata (from real data)"
    self.assertEqual(len(self.fm), self.test_file_md_count)

  def test_hdu_info(self):
    "Get HDUs summary info (from real data)"
    info = self.fm.hdu_info()
    self.assertNotEqual(info, None)
    self.assertEqual(len(info), 1)          # only one HDU
    self.assertEqual(info[0][0], 0)         # first HDU is zero
    self.assertTrue('PRIMARY' in info[0])   # and labeled as primary HDU

  def test_metadata(self):
    "Get metadata (from real data)"
    md = self.fm.metadata()
    self.assertNotEqual(md, None)
    self.assertEqual(len(md), self.test_file_md_count)

  def test_key_set(self):
    "Get the set of metadata keywords (from real data)"
    keys = self.fm.key_set()
    self.assertNotEqual(keys, None)
    # HISTORY keyword is repeated in test file:
    self.assertEqual(len(keys), self.test_file_md_count - 1)

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

  def test_metadata_as_json(self):
    "Get metadata as JSON (from real data)"
    jmd = self.fm.metadata_as_json()
    self.assertNotEqual(jmd, None)
    self.assertEqual(type(jmd), str)
    json_data = json.loads(jmd)
    self.assertEqual(type(json_data), list)
    self.assertEqual(type(json_data), list)
    self.assertEqual(len(json_data), self.test_file_md_count)
    self.assertTrue(all([type(j) == list for j in json_data]))
    self.assertTrue(all([len(j) == 2 for j in json_data]))


  def test_metadata_for_keys_default(self):
    "Get metadata for no keys specified: should get all keys (from real data)"
    md4k = self.fm.metadata_for_keys()
    self.assertNotEqual(md4k, None)
    self.assertEqual(len(md4k), self.test_file_md_count)

  def test_metadata_for_bad_keys(self):
    "Get metadata for nonexistant keys: should get no keys (from real data)"
    desired_keys = ["BADKEY", "NONE", "BOGUS"]
    md4k = self.fm.metadata_for_keys(set(desired_keys))
    self.assertNotEqual(md4k, None)
    self.assertEqual(type(md4k), list)
    self.assertEqual(len(md4k), 0)

  def test_metadata_for_one_key(self):
    "Get metadata for a single, unique key (from real data)"
    desired_keys = ["DATE"]
    md4k = self.fm.metadata_for_keys(set(desired_keys))
    self.assertNotEqual(md4k, None)
    self.assertEqual(type(md4k), list)
    self.assertEqual(len(md4k), 1)

  def test_metadata_for_keys(self):
    "Get all metadata for just the given non-duplicated keys (from real data)"
    desired_keys = ["NAXIS", "CRVAL2", "OBSERVAT"]
    md4k = self.fm.metadata_for_keys(set(desired_keys))
    self.assertNotEqual(md4k, None)
    self.assertEqual(len(md4k), len(desired_keys))

  def test_metadata_for_keys2(self):
    "Get all metadata for the possibly duplicated keys (from real data)"
    desired_keys = ["BITPIX", "CRVAL1", "HISTORY"]
    md4k = self.fm.metadata_for_keys(set(desired_keys))
    self.assertNotEqual(md4k, None)
    # HISTORY keyword is repeated in test file:
    self.assertEqual(len(md4k), 1+len(desired_keys))


  def test_filter_by_keys_none(self):
    "Filter metadata with empty key list should return empty list"
    fbk = self.fm.filter_by_keys([])
    self.assertNotEqual(fbk, None)
    self.assertEqual(type(fbk), list)
    self.assertEqual(len(fbk), 0)

  def test_filter_by_keys_bad(self):
    "Filter metadata with bogus keys list should return empty list"
    fbk = self.fm.filter_by_keys(["XXX", "YYY", "ZZZ"])
    self.assertNotEqual(fbk, None)
    self.assertEqual(type(fbk), list)
    self.assertEqual(len(fbk), 0)

  def test_filter_by_keys_one(self):
    "Filter metadata with single key list should return singleton list"
    fbk = self.fm.filter_by_keys(["NAXIS"])
    self.assertNotEqual(fbk, None)
    self.assertEqual(type(fbk), list)
    self.assertEqual(len(fbk), 1)
    self.assertTrue("NAXIS" in fbk[0].keyword)
    self.assertTrue(fbk[0].value, 941)

  def test_filter_by_keys_mult(self):
    "Filter metadata with good keys list should return good list"
    keys = ["BITPIX", "DATE"]
    fbk = self.fm.filter_by_keys(keys)
    self.assertNotEqual(fbk, None)
    self.assertEqual(type(fbk), list)
    self.assertEqual(len(fbk), len(keys))
    self.assertTrue(all([(item.keyword in keys) for item in fbk]))

  def test_filter_by_keys_mixed(self):
    "Filter metadata with mixed keys list should return good list"
    keys = ["BITPIX", "NAXIS", "BOGUSKEY", "NAXIS2", "DATE", "badkey"]
    fbk = self.fm.filter_by_keys(keys)
    self.assertNotEqual(fbk, None)
    self.assertEqual(type(fbk), list)
    self.assertEqual(len(fbk), 4)
    self.assertTrue(all([(item.keyword in keys) for item in fbk]))


  def test_default_cleaner(self):
    "The default cleaner function removes single quotes, double quotes, and backslashes"
    dirty = [ "\'B M\' E\'", "'B M' E'", '\"B M\" E\"', '"B M" E"', "\\B M\\ E\\", "\B M\ E\"" ]
    clean = [fm.default_cleaner_fn(v) for v in dirty]
    self.assertNotEqual(clean, None)
    self.assertTrue(all([v == "B M E" for v in clean]))


  def test_get_missing_key(self):
    "Throws exception on missing key"
    with self.assertRaises(TypeError):
      self.fm.get()

  def test_get_none(self):
    "Throws exception on None key"
    with self.assertRaises(TypeError):
      self.fm.get(None)

  def test_get_non_string(self):
    "Throws exception on non-string key"
    with self.assertRaises(TypeError):
      self.fm.get(88)

  def test_get_not_found_default(self):
    "Returns default of None on key not found"
    item = self.fm.get("NO_SUCH_KEY")
    self.assertEqual(item, None)

  def test_get_not_found_given(self):
    "Returns given value on key not found"
    item = self.fm.get("NO_SUCH_KEY", "HAPPY")
    self.assertNotEqual(item, None)
    self.assertEqual(item, "HAPPY")
    item = self.fm.get("NO_SUCH_KEY", 88)
    self.assertNotEqual(item, None)
    self.assertEqual(item, 88)

  def test_get_good(self):
    "Finds item for valid key"
    item = self.fm.get("NAXIS")
    self.assertNotEqual(item, None)
    self.assertEqual(type(item), fm.Metadatum)
    self.assertEqual(item.keyword, "NAXIS")
    self.assertEqual(item.value, 2)


  def test_getitem_none(self):
    "Throws exception on None key"
    with self.assertRaises(TypeError):
      self.fm[None]

  def test_getitem_non_string(self):
    "Throws exception on non-string key"
    with self.assertRaises(TypeError):
      self.fm[77]

  def test_getitem_not_found(self):
    "Throws exception on not found key"
    with self.assertRaises(KeyError):
      self.fm["NO_SUCH_KEY"]

  def test_getitem_good(self):
    "Finds item for valid key subscript"
    item = self.fm["NAXIS"]
    self.assertNotEqual(item, None)
    self.assertEqual(type(item), fm.Metadatum)
    self.assertEqual(item.keyword, "NAXIS")
    self.assertEqual(item.value, 2)


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
