#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe iRods Help class.
#   Written by: Tom Hicks. 6/30/2018.
#   Last Modified: Add one test for put_metaf. Rename empty file.
#
import unittest
from irods.session import iRODSSession
from irods.exception import CollectionDoesNotExist, DataObjectDoesNotExist

from context import ih                      # the module under test

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ConnectionsTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MovementTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FilesTestCase))
  # Tests in the following TestCase take about 15 seconds each to run:
  # suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(WalkTestCase))
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

  def test_cd_root_at_home(self):
    "Calling cd_root at user home does nothing"
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.helper.cd_root()                   # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertEqual(cwd1, cwd2)            # cwd should be unchanged

  def test_cd_root(self):
    "Move back to user home in the filesystem tree"
    self.helper.cd_down("xxx/yyy")          # "move down" in tree
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertNotEqual(cwd1, root1)        # cwd now moved from root
    self.helper.cd_root()                   # the test call
    root2 = self.helper.root()
    cwd2 = self.helper.cwd()
    self.assertEqual(root2, root1)          # root should be unchanged
    self.assertEqual(cwd2, root1)           # cwd returned to same as root


class FilesTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.helper = ih.IrodsHelper()          # create instance of class under test
    self.helper.connect({})                 # no options
    self.assertTrue(self.helper.is_connected())

  def tearDown(self):
    "Cleanup the test case"
    self.helper.disconnect()


  def test_set_mkdir(self):
    "Make a new directory and move into it"
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertEqual(cwd1, root1)
    id = self.helper.mkdir("testDir")       # the test call
    self.helper.cd_down("testDir")          # move into new subdir
    cwd2 = self.helper.cwd()
    self.assertNotEqual(cwd1, cwd2)

  def test_set_mkdir2(self):
    "Make multiple new directories and move to the bottom one"
    root1 = self.helper.root()
    cwd1 = self.helper.cwd()
    self.assertEqual(cwd1, root1)
    id = self.helper.mkdir("testDir/test/tmp") # the test call
    self.helper.cd_down("testDir/test/tmp")    # move into new subdir
    cwd2 = self.helper.cwd()
    self.assertNotEqual(cwd1, cwd2)


  def test_getf_bad_file_rel(self):
    "Throws exception on bad relative filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.helper.getf("BAD_FILENAME")

  def test_getf_bad_file_abs(self):
    "Throws exception on bad absolute filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.helper.getf("BAD_FILENAME", True)

  def test_getc_bad_dir_rel(self):
    "Throws exception on bad relative dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.helper.getc("BAD_DIRNAME")

  def test_getc_bad_dir_abs(self):
    "Throws exception on bad absolute dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.helper.getc("BAD_DIRNAME", True)


  def test_put_empty(self):
    "Upload an empty file to iRods home directory"
    filename = "empty.txt"
    self.helper.put(filename)               # the test call
    obj = self.helper.getf(filename)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, filename)

  def test_put_basic(self):
    "Upload a test file to iRods home directory"
    filename = "context.py"
    self.helper.put(filename)               # the test call
    obj = self.helper.getf(filename)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, filename)

  def test_put_after_cd(self):
    "Upload a test file to iRods in a newly created nested directory"
    filename = "context.py"
    dirpath = "testDir/test2"
    self.helper.mkdir(dirpath)
    self.helper.cd_down(dirpath)
    self.helper.put(filename)               # the test call
    obj = self.helper.getf(filename)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, filename)

  def test_put_nested(self):
    "Upload a test file to iRods in a newly created nested directory"
    dirpath = "testDir/test2"
    filename = "context.py"
    filepath = "{}/{}".format(dirpath, filename)
    self.helper.mkdir(dirpath)
    self.helper.put(filename, to_dir=dirpath)     # the test call
    obj = self.helper.getf(filepath, absolute=True)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, filename)


  def test_get_metac_bad_dir_rel(self):
    "Throws exception on bad relative dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.helper.get_metac("BAD_DIRNAME")

  def test_get_metac_bad_dir_abs(self):
    "Throws exception on bad absolute dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.helper.get_metac("BAD_DIRNAME", True)

  def test_get_metac(self):
    "Make a directory and then get metadata for it"
    dirpath = "testDir"
    self.helper.mkdir(dirpath)
    md = self.helper.get_metac(dirpath)
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)

  def test_get_metaf_bad_file_rel(self):
    "Throws exception on bad relative filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.helper.get_metaf("BAD_FILENAME")

  def test_get_metaf_bad_file_abs(self):
    "Throws exception on bad absolute filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.helper.get_metaf("BAD_FILENAME", True)

  def test_get_metaf_abs(self):
    "Put a file and then get metadata for it using absolute path"
    dirpath = "testDir"
    filename = "context.py"
    filepath = "{}/{}".format(dirpath, filename)
    self.helper.mkdir(dirpath)
    self.helper.put(filename, dirpath)
    md = self.helper.get_metaf(filepath, absolute=True) # the test call
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)

  def test_get_metaf_rel(self):
    "Put a file and then get metadata for it using relative path"
    dirpath = "testDir"
    filename = "context.py"
    self.helper.mkdir(dirpath)
    self.helper.cd_down(dirpath)
    self.helper.put(filename)
    md = self.helper.get_metaf(filename)    # the test call
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)


  def test_put_metaf_rel(self):
    "Create a file and then put metadata on it using a relative path"
    dirpath = "testDir"
    filename = "context.py"
    mdata = [ ("Key1", "Value1"), ("KEY2", "VALUE2"), ("BIG_KEY3", "Three of Hearts") ]
    mdata2 = [ ("Key1", "NewValue1"), ("KEY2", "NEW_VALUE2"), ("BIG_KEY3", "NO TRUMP") ]
    self.helper.mkdir(dirpath)
    self.helper.cd_down(dirpath)
    self.helper.put(filename)
    md0 = self.helper.get_metaf(filename)
    # print("\nMD0=", *md0, sep="\n")

    self.helper.put_metaf(filename, mdata)  # the test call
    md1 = self.helper.get_metaf(filename)
    # print("\nMD1=", *md1, sep="\n")
    self.assertNotEqual(md1, None)
    self.assertEqual(type(md1), list)
    self.assertTrue(len(md1) > len(mdata))
    self.assertNotEqual(md0, md1)

    self.helper.put_metaf(filename, mdata2)  # the test call
    md2 = self.helper.get_metaf(filename)
    # print("\nMD2=", *md2, sep="\n")
    self.assertNotEqual(md2, None)
    self.assertEqual(type(md2), list)
    self.assertTrue(len(md2) > len(mdata2))
    self.assertNotEqual(md1, md2)
    self.assertEqual(len(md1), len(md2))


  def test_get_cwd(self):
    """ Get dir info for the current working directory. """
    pwd = self.helper.cwd()
    dobj = self.helper.get_cwd()            # the test call
    self.assertNotEqual(dobj, None)
    self.assertEqual(dobj.path, pwd)

  def test_get_cwd_subdir(self):
    """ Get dir info for a subdirectory. """
    dirpath = "testDir"
    self.helper.mkdir(dirpath)
    self.helper.cd_down(dirpath)
    pwd = self.helper.cwd()
    dobj = self.helper.get_cwd()            # the test call
    self.assertNotEqual(dobj, None)
    self.assertEqual(dobj.name, dirpath)
    self.assertEqual(dobj.path, pwd)

  def test_get_root(self):
    """ Get dir info for the users root directory. """
    root = self.helper.root()
    dobj = self.helper.get_root()            # the test call
    self.assertNotEqual(dobj, None)
    self.assertEqual(dobj.path, root)


class WalkTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.helper = ih.IrodsHelper()          # create instance of class under test
    self.helper.connect({})                 # connect: no special options
    self.assertTrue(self.helper.is_connected()) # sanity check: assert connected
    filename = "context.py"                 # build a test directory tree
    filename2 = "metadata-keys.txt"
    self.helper.mkdir("test0/test1/test3")
    self.helper.mkdir("test0/test1/test4")
    self.helper.mkdir("test0/test2/test5")
    self.helper.put(filename, to_dir="test0/test1")
    self.helper.put(filename, to_dir="test0/test1/test3")
    self.helper.put(filename, to_dir="test0/test2/test5")
    self.helper.put(filename2, to_dir="test0/test2/test5")
    self.helper.cd_down("test0")

  def tearDown(self):
    "Cleanup the test case"
    self.helper.disconnect()


  def test_walk_topdown(self):
    """ Walk a directory tree in top-down order. """
    walker = self.helper.walk()             # the test call

    node = next(walker)
    self.assertEqual(node[0].name, "test0") # dir
    self.assertEqual(len(node[1]), 2)       # subdirs
    self.assertEqual(len(node[2]), 0)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test1") # dir
    self.assertEqual(len(node[1]), 2)       # subdirs
    self.assertEqual(len(node[2]), 1)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test3") # dir
    self.assertEqual(len(node[1]), 0)       # subdirs
    self.assertEqual(len(node[2]), 1)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test4") # dir
    self.assertEqual(len(node[1]), 0)       # subdirs
    self.assertEqual(len(node[2]), 0)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test2") # dir
    self.assertEqual(len(node[1]), 1)       # subdirs
    self.assertEqual(len(node[2]), 0)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test5") # dir
    self.assertEqual(len(node[1]), 0)       # subdirs
    self.assertEqual(len(node[2]), 2)       # files

    # for node in walker:
    #   print("\nDIR: {}".format(node[0]))
    #   print("SUBDIRS:")
    #   for n in node[1]:
    #     print("     {}".format(n))
    #   print("FILES:")
    #   for o in node[2]:
    #     print("     {}".format(o))


  def test_walk_bottomup(self):
    """ Walk a directory tree in bottom-up order. """
    walker = self.helper.walk(topdown=False) # the test call

    node = next(walker)
    self.assertEqual(node[0].name, "test3") # dir
    self.assertEqual(len(node[1]), 0)       # subdirs
    self.assertEqual(len(node[2]), 1)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test4") # dir
    self.assertEqual(len(node[1]), 0)       # subdirs
    self.assertEqual(len(node[2]), 0)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test1") # dir
    self.assertEqual(len(node[1]), 2)       # subdirs
    self.assertEqual(len(node[2]), 1)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test5") # dir
    self.assertEqual(len(node[1]), 0)       # subdirs
    self.assertEqual(len(node[2]), 2)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test2") # dir
    self.assertEqual(len(node[1]), 1)       # subdirs
    self.assertEqual(len(node[2]), 0)       # files

    node = next(walker)
    self.assertEqual(node[0].name, "test0") # dir
    self.assertEqual(len(node[1]), 2)       # subdirs
    self.assertEqual(len(node[2]), 0)       # files

    # for node in walker:
    #   print("\nDIR: {}".format(node[0]))
    #   print("SUBDIRS:")
    #   for n in node[1]:
    #     print("     {}".format(n))
    #   print("FILES:")
    #   for o in node[2]:
    #     print("     {}".format(o))


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
