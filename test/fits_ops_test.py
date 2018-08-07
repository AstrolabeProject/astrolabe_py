#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Operations module.
#   Written by: Tom Hicks. 6/22/2018.
#   Last Modified: Update for project rename.
#
import unittest
from astropy.io import fits

from context import fo                      # the module under test
from context import fm
from astrolabe_py import Metadatum
from astrolabe_py.fits_meta import FILEPATH_KEY

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(HandleCtypeMappingTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(HandleAltMappingTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FitsMetadataTestCase))
  return suite


class FitsOpsTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = {}
    cls.test_file = "resources/cvnidwabcut.fits"
    cls.test_file2 = "resources/m13.fits"
    cls.test_file_md_count = 64
    cls.test_dir = "resources"
    cls.test_dir_file_count = 4
    cls.empty_dir = "resources/empty_dir"
    cls.test_warn_count = 1                 # M13 test file has no warnings


class HandleCtypeMappingTestCase(FitsOpsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.fmeta = fm.FitsMeta(self.test_file)


  def test_ctype_no_ks(self):
    "Test valid CTYPE item with RA, no keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    self.assertNotIn("declination", mdk0)
    self.assertNotIn("right_ascension", mdk0)
    fo._handle_ctype_mapping(self.fmeta, Metadatum("CTYPE1", "RA--TAN"), [])
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertNotIn("declination", mdk1)
    self.assertIn("right_ascension", mdk1)

  def test_swapped_ctype_no_ks(self):
    "Test valid CTYPE item with DEC, no keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    self.assertNotIn("declination", mdk0)
    self.assertNotIn("right_ascension", mdk0)
    fo._handle_ctype_mapping(self.fmeta, Metadatum("CTYPE1", "DEC--TAN"), [])
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("declination", mdk1)
    self.assertNotIn("right_ascension", mdk1)

  def test_ctype_ks(self):
    "Test valid CTYPE item with RA, keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["NAXIS"]
    self.assertNotIn("declination", mdk0)
    self.assertNotIn("right_ascension", mdk0)
    fo._handle_ctype_mapping(self.fmeta, Metadatum("CTYPE1", "RA--TAN"), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertNotIn("declination", mdk1)
    self.assertNotIn("declination", ksub)
    self.assertIn("right_ascension", mdk1)
    self.assertIn("right_ascension", ksub)

  def test_swapped_ctype_ks(self):
    "Test valid CTYPE item with DEC, keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["NAXIS"]
    self.assertNotIn("declination", mdk0)
    self.assertNotIn("right_ascension", mdk0)
    fo._handle_ctype_mapping(self.fmeta, Metadatum("CTYPE1", "DEC--TAN"), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertNotIn("right_ascension", mdk1)
    self.assertNotIn("right_ascension", ksub)
    self.assertIn("declination", mdk1)
    self.assertIn("declination", ksub)



class HandleAltMappingTestCase(FitsOpsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.fmeta = fm.FitsMeta(self.test_file)

  def test_bogus_key_no_ks(self):
    "Test bogus item, no keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    self.assertNotIn("BOGUS", mdk0)
    fo._handle_alternate_key(self.fmeta, Metadatum("BOGUS", 2), [])
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertNotIn("BOGUS", mdk1)

  def test_non_altkey_no_ks(self):
    "Test standard item, no keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    self.assertIn("NAXIS", mdk0)
    fo._handle_alternate_key(self.fmeta, Metadatum("NAXIS", 2), [])
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("NAXIS", mdk1)

  def test_altkey_no_ks(self):
    "Test alternate key item, no keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    self.assertIn("OBJECT", mdk0)
    self.assertNotIn("obs_title", mdk0)
    fo._handle_alternate_key(self.fmeta, Metadatum("OBJECT", "Chandra"), [])
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("OBJECT", mdk1)
    self.assertIn("obs_title", mdk1)


  def test_bogus_key_ks_notinks(self):
    "Test bogus item, bogus key NOT in keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["NAXIS"]
    self.assertIn("NAXIS", ksub)            # in key subset
    self.assertNotIn("BOGUS", ksub)         # NOT in key subset
    self.assertNotIn("BOGUS", mdk0)         # NOT in original metadata
    fo._handle_alternate_key(self.fmeta, Metadatum("BOGUS", 2), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("NAXIS", ksub)            # still in key subset
    self.assertNotIn("BOGUS", ksub)         # still NOT in key subset
    self.assertNotIn("BOGUS", mdk1)         # still NOT in metadata

  def test_bogus_key_ks_inks(self):
    "Test bogus item, bogus key in keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["BOGUS"]
    self.assertIn("BOGUS", ksub)            # in key subset
    self.assertNotIn("BOGUS", mdk0)         # NOT in original metadata
    fo._handle_alternate_key(self.fmeta, Metadatum("BOGUS", 2), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("BOGUS", ksub)            # still in key subset
    self.assertNotIn("BOGUS", mdk1)         # still NOT in metadata

  def test_non_altkey_ks_notinks(self):
    "Test standard item, key NOT in keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["ZZZ"]
    self.assertIn("ZZZ", ksub)              # in key subset
    self.assertIn("NAXIS", mdk0)            # in original metadata
    self.assertNotIn("ZZZ", mdk0)           # NOT in original metadata
    fo._handle_alternate_key(self.fmeta, Metadatum("NAXIS", 2), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("ZZZ", ksub)              # still in key subset
    self.assertIn("NAXIS", mdk1)            # still in metadata
    self.assertNotIn("ZZZ", mdk1)           # still NOT in metadata

  def test_non_altkey_ks_inks(self):
    "Test standard item, key in keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["ZZZ", "NAXIS"]
    self.assertIn("ZZZ", ksub)              # in key subset
    self.assertIn("NAXIS", ksub)            # in key subset
    self.assertIn("NAXIS", mdk0)            # in original metadata
    self.assertNotIn("ZZZ", mdk0)           # NOT in original metadata
    fo._handle_alternate_key(self.fmeta, Metadatum("NAXIS", 2), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("ZZZ", ksub)              # still in key subset
    self.assertIn("NAXIS", ksub)            # still in key subset
    self.assertIn("NAXIS", mdk1)            # still in metadata
    self.assertNotIn("ZZZ", mdk1)           # still NOT in metadata


  def test_altkey_ks_notinks(self):
    "Test alternate key item, key NOT in keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["NAXIS", "ZZZ"]
    self.assertIn("NAXIS", ksub)            # in key subset
    self.assertIn("ZZZ", ksub)              # in key subset
    self.assertNotIn("OBJECT", ksub)        # NOT in key subset
    self.assertNotIn("obs_title", ksub)     # NOT in key subset
    self.assertIn("NAXIS", mdk0)            # in original metadata
    self.assertIn("OBJECT", mdk0)           # in original metadata
    self.assertNotIn("ZZZ", mdk0)           # NOT in original metadata
    self.assertNotIn("obs_title", mdk0)     # NOT in original metadata
    fo._handle_alternate_key(self.fmeta, Metadatum("OBJECT", "Chandra"), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("NAXIS", ksub)            # still in key subset
    self.assertIn("ZZZ", ksub)              # still in key subset
    self.assertNotIn("OBJECT", ksub)        # still NOT in key subset
    self.assertNotIn("obs_title", ksub)     # still NOT in key subset
    self.assertIn("NAXIS", mdk1)            # still in metadata
    self.assertIn("OBJECT", mdk1)           # still in metadata
    self.assertNotIn("ZZZ", mdk1)           # still NOT in metadata
    self.assertNotIn("obs_title", mdk1)     # still NOT in metadata

  def test_altkey_ks_inks(self):
    "Test alternate key item, key in keys subset"
    md0 = self.fmeta.metadata()
    mdk0 = [md[0] for md in md0]
    ksub = ["OBJECT", "ZZZ"]
    self.assertIn("OBJECT", ksub)           # in key subset
    self.assertIn("ZZZ", ksub)              # in key subset
    self.assertNotIn("obs_title", ksub)     # NOT in key subset
    self.assertIn("OBJECT", mdk0)           # in original metadata
    self.assertNotIn("ZZZ", mdk0)           # NOT in original metadata
    self.assertNotIn("obs_title", mdk0)     # NOT in original metadata
    fo._handle_alternate_key(self.fmeta, Metadatum("OBJECT", "Chandra"), ksub)
    md1 = self.fmeta.metadata()
    mdk1 = [md[0] for md in md1]
    self.assertIn("OBJECT", ksub)           # still in key subset
    self.assertIn("ZZZ", ksub)              # still in key subset
    self.assertIn("obs_title", ksub)        # now added to key subset
    self.assertIn("OBJECT", mdk1)           # still in metadata
    self.assertNotIn("ZZZ", mdk1)           # still NOT in metadata
    self.assertIn("obs_title", mdk1)        # now added to metdata



class FitsMetadataTestCase(FitsOpsTestCase):

  def setUp(self):
    "Initialize the test case"
    pass

  def test_bad_filepath(self):
    "Throws exception on bad file path"
    self.assertRaises(FileNotFoundError,
                      fo.fits_metadata, "NO_SUCH_FILEPATH", self.default_options)


  def test_no_md_keys(self):
    "Extract all metadata if no keys_subset specified"
    metadata = fo.fits_metadata(self.test_file)
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), self.test_file_md_count)
    mdkeys = [md[0] for md in metadata]
    self.assertIn(FILEPATH_KEY, mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)

  def test_md_standard_keys(self):
    "Standard keys are extracted to metadata"
    metadata = fo.fits_metadata(self.test_file)
    # [print(item) for item in metadata]      # DEBUGGING
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), self.test_file_md_count)
    mdkeys = [md[0] for md in metadata]
    self.assertIn(FILEPATH_KEY, mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    self.assertIn("NAXIS", mdkeys)
    self.assertIn("NAXIS1", mdkeys)
    self.assertIn("NAXIS2", mdkeys)
    self.assertIn("DATE-OBS", mdkeys)
    self.assertIn("INSTRUME", mdkeys)
    self.assertIn("OBJECT", mdkeys)
    self.assertIn("OBSERVER", mdkeys)
    self.assertIn("ORIGIN", mdkeys)

  def test_md_alternate_keys(self):
    "Alternate keys are computed and added to metadata"
    metadata = fo.fits_metadata(self.test_file)
    # [print(item) for item in metadata]      # DEBUGGING
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), self.test_file_md_count)
    mdkeys = [md[0] for md in metadata]
    self.assertIn(FILEPATH_KEY, mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    self.assertIn("obs_title", mdkeys)
    self.assertIn("spatial_axis_1_number_bins", mdkeys)
    self.assertIn("spatial_axis_2_number_bins", mdkeys)
    self.assertIn("start_time", mdkeys)
    self.assertIn("facility_name", mdkeys)
    self.assertIn("obs_creator_name", mdkeys)
    self.assertIn("obs_title", mdkeys)


  def test_keys_subset_empty(self):
    "Extract all metadata if keys_subset is empty"
    metadata = fo.fits_metadata(self.test_file, {"keys_subset": []})
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), self.test_file_md_count)
    mdkeys = [md[0] for md in metadata]
    self.assertIn(FILEPATH_KEY, mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)

  def test_keys_subset_1(self):
    "Extract metadata for singleton keys_subset"
    ksubset = ["ORIGIN"]
    ks_len = 2 + len(ksubset)               # RA and DEC added automatically
    metadata = fo.fits_metadata(self.test_file, {"keys_subset": ksubset})
    self.assertNotEqual(metadata, None)
    # [print(item) for item in metadata]      # DEBUGGING
    self.assertEqual(len(metadata), ks_len)
    mdkeys = [md[0] for md in metadata]
    self.assertNotIn(FILEPATH_KEY, mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    for key in ksubset:
      self.assertIn(key, mdkeys)

  def test_keys_subset_no_alt(self):
    "Extract metadata for specified keys_subset which has no alternative keys"
    ksubset = ["CRPIX1", "CRPIX2", "ELEVATIO", "AIRMASS"]
    ks_len = 2 + len(ksubset)               # RA and DEC added automatically
    metadata = fo.fits_metadata(self.test_file, {"keys_subset": ksubset})
    self.assertNotEqual(metadata, None)
    # [print(item) for item in metadata]      # DEBUGGING
    self.assertEqual(len(metadata), ks_len)
    mdkeys = [md[0] for md in metadata]
    self.assertNotIn(FILEPATH_KEY, mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    for key in ksubset:
      self.assertIn(key, mdkeys)

  def test_keys_subset_all_alt(self):
    "Extract metadata for specified keys_subset, all of which have alternative keys"
    ksubset = ["NAXIS1", "NAXIS2", "DATE-OBS", "INSTRUME"]
    ks_len = 2 + (2 * len(ksubset))         # RA and DEC added automatically
    metadata = fo.fits_metadata(self.test_file, {"keys_subset": ksubset})
    self.assertNotEqual(metadata, None)
    # [print(item) for item in metadata]      # DEBUGGING
    self.assertEqual(len(metadata), ks_len)
    mdkeys = [md[0] for md in metadata]
    self.assertNotIn(FILEPATH_KEY, mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    for key in ksubset:
      self.assertIn(key, mdkeys)


  def test_ignore_no_keys(self):
    "Extract all metadata if no ignore keys specified"
    metadata = fo.fits_metadata(self.test_file) # the test call
    self.assertNotEqual(metadata, None)
    # for md in metadata:
    #   print("{}: {}".format(md.keyword, md.value))
    self.assertEqual(len(metadata), self.test_file_md_count)
    mdkeys = [md[0] for md in metadata]
    self.assertIn(FILEPATH_KEY, mdkeys)
    self.assertIn("HISTORY", mdkeys)        # should be present
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    self.assertIn("NAXIS", mdkeys)          # some standard keys
    self.assertIn("INSTRUME", mdkeys)
    self.assertIn("OBSERVER", mdkeys)
    self.assertIn("OBJECT", mdkeys)
    self.assertIn("facility_name", mdkeys)  # derived from standard keys
    self.assertIn("obs_creator_name", mdkeys)
    self.assertIn("obs_title", mdkeys)

  def test_ignore1_key(self):
    "Do not extract metadata for ignored key"
    options = { "ignore_keys": ["HISTORY"], "verbose": True }
    metadata = fo.fits_metadata(self.test_file, options) # the test call
    self.assertNotEqual(metadata, None)
    # for md in metadata:
    #   print("{}: {}".format(md.keyword, md.value))
    self.assertEqual(len(metadata), self.test_file_md_count - 2) # HISTORY twice in test file
    mdkeys = [md[0] for md in metadata]
    self.assertIn(FILEPATH_KEY, mdkeys)
    self.assertNotIn("HISTORY", mdkeys)     # should be ignored
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    self.assertIn("NAXIS", mdkeys)          # some standard keys
    self.assertIn("INSTRUME", mdkeys)
    self.assertIn("OBSERVER", mdkeys)
    self.assertIn("OBJECT", mdkeys)
    self.assertIn("facility_name", mdkeys)  # derived from standard keys
    self.assertIn("obs_creator_name", mdkeys)
    self.assertIn("obs_title", mdkeys)

  def test_ignoreN_keys(self):
    "Do not extract metadata for ignored keys"
    options = { "ignore_keys": ["NAXIS", "INSTRUME", "obs_title", "CDELT1"], "verbose": True }
    metadata = fo.fits_metadata(self.test_file, options) # the test call
    self.assertNotEqual(metadata, None)
    # for md in metadata:
    #   print("{}: {}".format(md.keyword, md.value))
    self.assertEqual(len(metadata), self.test_file_md_count - 4)
    mdkeys = [md[0] for md in metadata]
    self.assertIn(FILEPATH_KEY, mdkeys)
    self.assertIn("HISTORY", mdkeys)        # should be present
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    self.assertNotIn("NAXIS", mdkeys)       # explicitly removed
    self.assertNotIn("CDELT1", mdkeys)      # explicitly removed
    self.assertIn("CDELT2", mdkeys)         # still present: unaffected by similar name
    self.assertNotIn("INSTRUME", mdkeys)    # explicitly removed
    self.assertNotIn("facility_name", mdkeys) # NOT present because INSTRUME explicitly removed
    self.assertIn("OBSERVER", mdkeys)
    self.assertIn("obs_creator_name", mdkeys) # derived from OBSERVER, so still present
    self.assertIn("OBJECT", mdkeys)
    self.assertIn("obs_title", mdkeys)      # derived from OBJECT, so still present


  def test_fits_hdu_info(self):
    "Get summary info report for the HDUs of a file"
    report = fo.fits_hdu_info(self.test_file)
    self.assertNotEqual(report, None)
    self.assertEqual(len(report), 3)        # filename, heading, and one HDU line
    self.assertTrue(all([type(line) == str for line in report]))

  def test_execute_info_one(self):
    "Get summary info reports for a single FITS files"
    reports = fo.execute_info({"images_path": self.test_file})
    self.assertNotEqual(reports, None)
    self.assertTrue(type(reports) == list)
    self.assertEqual(len(reports), 1)
    self.assertTrue(all([type(rpt) == list for rpt in reports]))
    for rpt in reports:
      self.assertEqual(len(rpt), 3)         # filename, heading, and one HDU line
      self.assertTrue(all([type(line) == str for line in rpt]))

  def test_execute_info_nofits(self):
    "Get no summary info reports in directory with no FITS files"
    reports = fo.execute_info({"images_path": self.empty_dir})
    self.assertNotEqual(reports, None)
    self.assertTrue(type(reports) == list)
    self.assertEqual(len(reports), 0)

  def test_execute_info(self):
    "Get summary info reports for several FITS files"
    reports = fo.execute_info({"images_path": self.test_dir})
    self.assertNotEqual(reports, None)
    self.assertTrue(type(reports) == list)
    self.assertEqual(len(reports), self.test_dir_file_count)
    self.assertTrue(all([type(rpt) == list for rpt in reports]))
    for rpt in reports:
      self.assertEqual(len(rpt), 3)         # filename, heading, and one HDU line
      self.assertTrue(all([type(line) == str for line in rpt]))


  def test_fits_verify(self):
    "Get verification report for a FITS file"
    report = fo.fits_verify(self.test_file)
    self.assertNotEqual(report, None)
    self.assertTrue(all([type(line) == str for line in report]))
    self.assertEqual(len(report), 6)        # filename, preamble, HDU#, Card#, ErrorMsg, Note

  def test_execute_verify_one(self):
    "Get verify reports for a single FITS files"
    reports = fo.execute_verify({"images_path": self.test_file})
    self.assertNotEqual(reports, None)
    self.assertTrue(type(reports) == list)
    self.assertEqual(len(reports), 1)
    self.assertTrue(all([type(rpt) == list for rpt in reports]))
    for rpt in reports:
      self.assertEqual(len(rpt), 6)        # filename, preamble, HDU#, Card#, ErrorMsg, Note
      self.assertTrue(all([type(line) == str for line in rpt]))

  def test_execute_verify_nofits(self):
    "Get no verify reports in directory with no FITS files"
    reports = fo.execute_verify({"images_path": self.empty_dir})
    self.assertNotEqual(reports, None)
    self.assertTrue(type(reports) == list)
    self.assertEqual(len(reports), 0)

  def test_execute_verify_nowarns(self):
    "Get no verify report from a FITS file with no problems"
    reports = fo.execute_verify({"images_path": self.test_file2})
    self.assertNotEqual(reports, None)
    self.assertTrue(type(reports) == list)
    self.assertEqual(len(reports), 0)

  def test_execute_verify(self):
    "Get verify reports for several FITS files"
    reports = fo.execute_verify({"images_path": self.test_dir})
    self.assertNotEqual(reports, None)
    self.assertTrue(type(reports) == list)
    self.assertEqual(len(reports), self.test_warn_count)
    self.assertTrue(all([type(rpt) == list for rpt in reports]))
    for rpt in reports:
      self.assertEqual(len(rpt), 6)        # filename, preamble, HDU#, Card#, ErrorMsg, Note
      self.assertTrue(all([type(line) == str for line in rpt]))


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
