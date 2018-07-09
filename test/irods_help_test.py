#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe iRods Help class.
#   Written by: Tom Hicks. 6/30/2018.
#   Last Modified: Consistent quotes and test doc strings.
#
import unittest
from irods.session import iRODSSession

from context import ih                      # the module under test

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ConnectionsTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MovementTestCase))
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
    self.helper = ih.IrodsHelper()            # create instance of class under test

  def tearDown(self):
    "Cleanup the test case"
    self.helper.disconnect()


  def test_helper(self):
    "The helper instance has been created"
    self.assertNotEqual(self.helper, None)

  def test_connect(self):
    "Make default connection"
    self.helper.connect({})                 # no options
    self.assertTrue(self.helper.is_connected())

  def test_connect_envfile(self):
    "Make connection using options specifying env file"
    self.helper.connect(self.default_options)
    self.assertTrue(self.helper.is_connected())

  def test_disconnect(self):
    "The connection has been closed"
    self.helper.disconnect()
    self.assertFalse(self.helper.is_connected())

  def test_get_session(self):
    "Get the session from the helper"
    self.helper.connect({})                 # no options
    sess = self.helper.session()
    self.assertNotEqual(sess, None)
    self.assertEqual(type(sess), iRODSSession)

  def test_get_cwd(self):
    "Get the current directory from the helper"
    self.helper.connect({})                 # no options
    cwd = self.helper.cwd()
    self.assertNotEqual(cwd, None)
    self.assertEqual(type(cwd), str)

  def test_get_root(self):
    "Get the root directory from the helper"
    self.helper.connect({})                 # no options
    root = self.helper.root()
    self.assertNotEqual(root, None)
    self.assertEqual(type(root), str)

  def test_cwd_is_root(self):
    "The initial working directory should be the root directory"
    self.helper.connect({})                 # no options
    root = self.helper.root()
    cwd = self.helper.cwd()
    self.assertEqual(cwd, root)


class MovementTestCase(IrodsHelpTestCase):

  # @classmethod
  # def setUpClass(cls):
  #   "Create some special test subdirectories, just for tests in this class"
  #   helper = ih.IrodsHelper()
  #   helper.connect({})                      # no options
  #   new_dir_path = "{}/test/tstsubdir".format(helper.root())
  #   new_dirs = helper.session().collections.create(new_dir_path)
  #   helper.disconnect()

  def setUp(self):
    "Initialize the test case"
    self.helper = ih.IrodsHelper()          # create instance of class under test
    self.helper.connect({})                 # no options
    self.assertTrue(self.helper.is_connected())

  def tearDown(self):
    "Cleanup the test case"
    self.helper.disconnect()


  def test_set_root(self):
    "Reset the root directory and test root and cwd"
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertEqual(cwd1, root1)
    self.helper.set_root()                  # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertEqual(cwd2, root2)
    self.assertEqual(cwd1, cwd2)
    self.assertEqual(root1, root2)

  def test_set_root2(self):
    "Reset the root directory and test root and cwd"
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertEqual(cwd1, root1)
    self.helper.set_root(top_dir="analyses") # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertNotEqual(root1, root2)
    self.assertNotEqual(cwd1, cwd2)
    self.assertEqual(cwd2, root2)

  def test_cd_down(self):
    "Move down in the filesystem tree"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertEqual(cwd1, root1)
    self.helper.cd_down("test")             # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    self.assertNotEqual(cwd2, root2)        # cwd changed from root

  def test_cd_down2(self):
    "Move down further in the filesystem tree"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertEqual(cwd1, root1)
    self.helper.cd_down("test/tstsubdir")   # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    self.assertNotEqual(cwd2, root2)        # cwd changed from root

  def test_cd_home_at_home(self):
    "Calling cd_home at user home does nothing"
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.helper.cd_home()                   # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertEqual(cwd1, cwd2)            # cwd should be unchanged

  def test_cd_home(self):
    "Move back to user home in the filesystem tree"
    self.helper.cd_down("xxx/yyy")          # "move down" in tree
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertNotEqual(cwd1, root1)        # cwd now moved from root
    self.helper.cd_home()                   # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertEqual(root2, root1)          # root should be unchanged
    self.assertEqual(cwd2, root1)           # cwd returned to same as root


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
