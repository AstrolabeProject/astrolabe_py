#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe iRods Help class.
#   Written by: Tom Hicks. 6/30/2018.
#   Last Modified: Initial creation.
#
import unittest
#from irods.session import iRODSSession

from context import ih                      # the module under test

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ConnectionsTestCase))
  return suite


class IrodsHelpTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = { "irods_env_file": "irods_env_file.json" }
    cls.irods_env_file = "irods_env_file.json"


class ConnectionsTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    pass

  def tearDown(self):
    "Cleanup the test case"
    pass

  def test_one(self):
    "Do some testing"
    self.assertEqual(self.irods_env_file, "irods_env_file.json") # REPLACE LATER


if __name__ == '__main__':
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
