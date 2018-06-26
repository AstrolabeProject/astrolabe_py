#!/usr/bin/env python3
#
# Python code to (unit) test the Astrolabe FITS Metadata module.
#   Written by: Tom Hicks. 6/22/2018.
#   Last Modified: Get Suite working correctly. Add tests of fits_metadata.
#
from astropy.io import fits
import astrolabe_uploader.fits_meta as fm
import unittest

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GetMetadataKeysTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(HandleCtypeMappingTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FitsMetadataTestCase))
  return suite


class FitsMetaTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = { "keyfile": "metadata-keys.txt" }
    cls.test_files = [ "cvnidwabcut.fits" ]


class GetMetadataKeysTestCase(FitsMetaTestCase):

  def setUp(self):
    "Initialize the test case"
    pass

  def test_bad_metdata_keyfile(self):
    "Throws exception on bad metadata key filename"
    self.assertRaises(FileNotFoundError, fm.get_metadata_keys, {"keyfile": "BAD_KEYFILE_NAME"})

  def test_empty_metadata_keys(self):
    "Return empty list of desired metadata keys"
    keys = fm.get_metadata_keys({"keyfile": "empty-metadata-keyfile.txt"})
    self.assertNotEqual(keys, None)
    self.assertEqual(len(keys), 0)
    self.assertNotIn("filepath", keys)

  def test_get_metadata_keys(self):
    "Gets a list of desired metadata keys from keyfile"
    keys = fm.get_metadata_keys(self.default_options)
    self.assertNotEqual(keys, None)
    self.assertEqual(len(keys), 52)
    self.assertIn("filepath", keys)


class HandleCtypeMappingTestCase(FitsMetaTestCase):

  def setUp(self):
    "Initialize the test case"
    datafile = fits.open(self.test_files[0])
    self.file_metadata = datafile[0].header
    datafile.close()

  def test_nocrval(self):
    metadata = []
    self.assertFalse(metadata)
    fm.handle_ctype_mapping('', self.file_metadata, metadata)
    fm.handle_ctype_mapping('BADKEY', self.file_metadata, metadata)
    self.assertFalse(metadata)

  def test_crval1(self):
    metadata = []
    self.assertFalse(metadata)
    fm.handle_ctype_mapping('CRVAL1', self.file_metadata, metadata)
    self.assertTrue(metadata)
    self.assertEqual(len(metadata), 2)
    self.assertTrue(all([isinstance(md, tuple) for md in metadata]))
    self.assertNotIn("CRVAL2", [md[0] for md in metadata])
    self.assertIn("right_ascension", [md[0] for md in metadata])

  def test_crval2(self):
    metadata = []
    self.assertFalse(metadata)
    fm.handle_ctype_mapping('CRVAL2', self.file_metadata, metadata)
    self.assertTrue(metadata)
    self.assertEqual(len(metadata), 2)
    self.assertTrue(all([isinstance(md, tuple) for md in metadata]))
    self.assertNotIn("CRVAL1", [md[0] for md in metadata])
    self.assertIn("declination", [md[0] for md in metadata])


class FitsMetadataTestCase(FitsMetaTestCase):

  def setUp(self):
    "Initialize the test case"
    pass

  def test_bad_filepath(self):
    "Throws exception on bad file path"
    self.assertRaises(FileNotFoundError,
                      fm.fits_metadata, "NO_SUCH_FILEPATH", self.default_options)

  def test_no_metadata_keys(self):
    "Extract no metadata if no metadata keys specified"
    mdata = fm.fits_metadata(self.test_files[0], {"keyfile": "empty-metadata-keyfile.txt"})
    self.assertNotEqual(mdata, None)
    self.assertEqual(len(mdata), 0)
    self.assertNotIn("filepath", mdata)

  def test_metadata(self):
    "Extract metadata if default metadata keys specified"
    metadata = fm.fits_metadata(self.test_files[0], self.default_options)
    # print(metadata)                         # DEBUGGING
    self.assertNotEqual(metadata, None)
    self.assertEqual(len(metadata), 17)

    mdkeys = [md[0] for md in metadata]
    self.assertIn("filepath", mdkeys)
    self.assertIn("right_ascension", mdkeys)
    self.assertIn("declination", mdkeys)
    self.assertIn("obs_title", mdkeys)
    self.assertIn("ORIGIN", mdkeys)


if __name__ == '__main__':
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
