#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe iRods Help class.
#   Written by: Tom Hicks. 6/30/2018.
#   Last Modified: Add some connection tests.
#
import unittest
from irods.session import iRODSSession

from context import ih                      # the module under test

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ConnectionsTestCase))
  return suite


class IrodsHelpTestCase(unittest.TestCase):

  """ Base test class """
  @classmethod
  def setUpClass(cls):
    cls.default_options = { "irods_env_file": "irods_env_file.json" }
    cls.irods_env_file = "irods_env_file.json"


class ConnectionsTestCase(IrodsHelpTestCase):

  def setUp(self):
    """ Initialize the test case """
    self.helper = ih.IrodsHelper()            # create instance of class under test

  def tearDown(self):
    """ Cleanup the test case """
    self.helper.disconnect()

  def test_helper(self):
    """ Test that the helper instance has been created. """
    self.assertNotEqual(self.helper, None)

  def test_connected(self):
    """ Test that the helper is connected (a session has been created). """
    self.helper.connect({})                 # no options
    self.assertTrue(self.helper.is_connected())

  def test_disconnect(self):
    """ Test that the connection has been closed """
    self.helper.disconnect()
    self.assertFalse(self.helper.is_connected())

  def test_get_session(self):
    """ Test getting the session from the helper. """
    self.helper.connect({})                 # no options
    sess = self.helper.session()
    self.assertNotEqual(sess, None)
    self.assertEqual(type(sess), iRODSSession)

  def test_get_cwd(self):
    """ Test getting the current directory from the helper. """
    self.helper.connect({})                 # no options
    cwd = self.helper.cwd()
    self.assertNotEqual(cwd, None)
    self.assertEqual(type(cwd), str)


if __name__ == '__main__':
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
