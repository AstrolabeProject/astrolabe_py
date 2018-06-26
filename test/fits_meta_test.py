# #!/usr/bin/env python3
#
# Python code to (unit) test the Astrolabe FITS Metadata module.
#   Written by: Tom Hicks. 6/22/2018.
#   Last Modified: Initial creation.
#
import astrolabe_uploader.fits_meta as fm
import unittest

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.TestLoader().loadTestsFromTestCase(GetMetadataKeysTestCase))
  return suite


class FitsMetaTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = { "keyfile": "metadata-keys.txt" }


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


if __name__ == '__main__':
  suite = suite()
  unittest.TextTestRunner(verbosity = 2).run(suite)
