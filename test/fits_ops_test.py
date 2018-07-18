#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe FITS Operations module.
#   Written by: Tom Hicks. 6/22/2018.
#   Last Modified: WIP: begin rewrite for rewritten fits_ops module.
#
import unittest
from astropy.io import fits

from context import fo                      # the module under test
from astrolabe_uploader.fits_meta import FILEPATH_KEY


def suite():
  suite = unittest.TestSuite()
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(HandleCtypeMappingTestCase))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExtractMetadataTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FitsOpsdataTestCase))
  return suite


class FitsOpsTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = {}
    cls.test_file = "cvnidwabcut.fits"
    cls.test_file_md_count = 63


class HandleCtypeMappingTestCase(FitsOpsTestCase):

  def setUp(self):
    "Initialize the test case"
    datafile = fits.open(self.test_file)
    self.file_metadata = datafile[0].header
    datafile.close()

  def test_nocrval(self):
    "Handle missing or bad CRVAL key strings"
    metadata = []
    self.assertFalse(metadata)
    fo.handle_ctype_mapping("", self.file_metadata, metadata)
    fo.handle_ctype_mapping("BADKEY", self.file_metadata, metadata)
    self.assertFalse(metadata)

  def test_crval1(self):
    "Interpret CRVAL1 metadata item from real data"
    metadata = []
    self.assertFalse(metadata)
    fo.handle_ctype_mapping("CRVAL1", self.file_metadata, metadata)
    self.assertTrue(metadata)
    self.assertEqual(len(metadata), 2)
    self.assertTrue(all([isinstance(md, tuple) for md in metadata]))
    self.assertNotIn("CRVAL2", [md[0] for md in metadata])
    self.assertIn("right_ascension", [md[0] for md in metadata])

  def test_crval2(self):
    "Interpret CRVAL2 metadata item from real data"
    metadata = []
    self.assertFalse(metadata)
    fo.handle_ctype_mapping("CRVAL2", self.file_metadata, metadata)
    self.assertTrue(metadata)
    self.assertEqual(len(metadata), 2)
    self.assertTrue(all([isinstance(md, tuple) for md in metadata]))
    self.assertNotIn("CRVAL1", [md[0] for md in metadata])
    self.assertIn("declination", [md[0] for md in metadata])

  def test_swapped_crval1(self):
    "Interpret CRVAL1 metadata item with swapped CTYPE value"
    metadata = []
    self.assertFalse(metadata)
    self.file_metadata["CTYPE1"] = "DEC--TAN"    # alter incoming metadata
    fo.handle_ctype_mapping("CRVAL1", self.file_metadata, metadata)
    self.assertTrue(metadata)
    self.assertEqual(len(metadata), 2)
    self.assertTrue(all([isinstance(md, tuple) for md in metadata]))
    self.assertNotIn("CRVAL2", [md[0] for md in metadata])
    self.assertIn("declination", [md[0] for md in metadata])

  def test_swapped_crval2(self):
    "Interpret CRVAL2 metadata item with swapped CTYPE value"
    metadata = []
    self.assertFalse(metadata)
    self.file_metadata["CTYPE2"] = "RA--TAN"    # alter incoming metadata
    fo.handle_ctype_mapping("CRVAL2", self.file_metadata, metadata)
    self.assertTrue(metadata)
    self.assertEqual(len(metadata), 2)
    self.assertTrue(all([isinstance(md, tuple) for md in metadata]))
    self.assertNotIn("CRVAL1", [md[0] for md in metadata])
    self.assertIn("right_ascension", [md[0] for md in metadata])


class ExtractMetadataTestCase(FitsOpsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.hduList = fits.open(self.test_file)

  def tearDown(self):
    self.hduList.close()

  def test_no_metadata_keys(self):
    "Extract no metadata if no metadata keys specified"
    metadata = fo.extract_metadata(self.test_file, self.hduList, [])  # no desired keys
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), 0)
    self.assertNotIn(FILEPATH_KEY, metadata)

  def test_filepath_key(self):
    "Extract file path, if special FILEPATH_KEY is given"
    metadata = fo.extract_metadata(self.test_file, self.hduList, [FILEPATH_KEY])
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), 1)
    self.assertIn(FILEPATH_KEY, [md[0] for md in metadata])

  def test_an_alternate_key(self):
    "Extract metadata for the given alternate key"
    metadata = fo.extract_metadata(self.test_file, self.hduList, ["obs_creator_name"])
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), 1)
    self.assertIn("obs_creator_name", [md[0] for md in metadata])

  def test_CRVAL_keys(self):
    "Extract metadata for the given CRVAL* keys"
    metadata = fo.extract_metadata(self.test_file, self.hduList, ["CRVAL1", "CRVAL2"])
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), 4)
    mdkeys = [md[0] for md in metadata]
    self.assertIn("declination", mdkeys)
    self.assertIn("CRVAL1", mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("CRVAL2", mdkeys)

  def test_normal_key(self):
    "Extract metadata key for the given normal key"
    metadata = fo.extract_metadata(self.test_file, self.hduList, ["SIMPLE"])
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), 1)
    self.assertIn("SIMPLE", [md[0] for md in metadata])


class FitsOpsdataTestCase(FitsOpsTestCase):

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
    self.assertIn("obs_title", mdkeys)
    self.assertIn("spatial_axis_1_number_bins", mdkeys)
    self.assertIn("spatial_axis_2_number_bins", mdkeys)
    self.assertIn("start_time", mdkeys)
    self.assertIn("facility_name", mdkeys)
    self.assertIn("obs_creator_name", mdkeys)
    self.assertIn("obs_title", mdkeys)


  def test_fits_hdu_info(self):
    "Get summary info report for the HDUs of a file"
    report = fo.fits_hdu_info(self.test_file)
    self.assertNotEqual(report, None)
    self.assertEqual(len(report), 3)        # filename, heading, one HDU line
    self.assertTrue(all([type(line) == str for line in report]))


  def test_fits_verify(self):
    "Get verification report for the HDUs of a file"
    report = fo.fits_verify(self.test_file)
    self.assertNotEqual(report, None)
    self.assertTrue(all([type(line) == str for line in report]))
    self.assertEqual(len(report), 6)        # Filename, preamble, HDU#, Card#, ErrorMsg, Note


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
