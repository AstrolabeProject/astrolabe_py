#!/usr/bin/env python3
#
# Python code to unit test the Astrolabe iRods Help class.
#   Written by: Tom Hicks. 6/30/2018.
#   Last Modified: Rename ihelper, for consistency. Add tests for cd method. Update for get_dir rename.
#
import os
import unittest
from irods.session import iRODSSession
from irods.exception import CollectionDoesNotExist, DataObjectDoesNotExist

from context import ih                      # the module under test
from context import up
from astrolabe_uploader import Metadatum

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ConnectionsTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MovementTestCase))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FilesTestCase))
  # Tests in the following TestCase take about 15 seconds each to run:
  # suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(WalkTestCase))
  # Tests in the following TestCase take about 5 minutes each to run:
  # suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DeleteTestCase))
  return suite


class IrodsHelpTestCase(unittest.TestCase):

  "Base test class"
  @classmethod
  def setUpClass(cls):
    cls.default_options = { "irods_env_file": "irods_env_file.json" }
    cls.irods_env_file = "irods_env_file.json"
    cls.root_dir = up._ASTROLABE_ROOT_DIR


class ConnectionsTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = None

  def tearDown(self):
    "Cleanup the test case"
    self.ihelper.disconnect()


  def test_connect_ctor(self):
    "A default connection is made by the constructor"
    self.ihelper = ih.IrodsHelper()
    self.assertNotEqual(self.ihelper, None)
    self.assertTrue(self.ihelper.is_connected())

  def test_connect(self):
    "Make default connection"
    self.ihelper = ih.IrodsHelper(connect=False) # do not connect in ctor
    self.assertNotEqual(self.ihelper, None)
    self.ihelper.connect()                       # connect explicitly
    self.assertTrue(self.ihelper.is_connected())

  def test_connect_envfile(self):
    "Make connection using options specifying env file"
    self.ihelper = ih.IrodsHelper(options=self.default_options)
    self.assertNotEqual(self.ihelper, None)
    self.assertTrue(self.ihelper.is_connected())

  def test_disconnect(self):
    "Open connection and then close it"
    self.ihelper = ih.IrodsHelper()
    self.assertNotEqual(self.ihelper, None)
    self.assertTrue(self.ihelper.is_connected())
    self.ihelper.disconnect()
    self.assertFalse(self.ihelper.is_connected())

  def test_get_session(self):
    "Get the session from the helper"
    self.ihelper = ih.IrodsHelper()
    self.assertNotEqual(self.ihelper, None)
    sess = self.ihelper.session()
    self.assertNotEqual(sess, None)
    self.assertEqual(type(sess), iRODSSession)

  def test_get_cwd(self):
    "Get the current directory from the helper"
    self.ihelper = ih.IrodsHelper()
    self.assertNotEqual(self.ihelper, None)
    cwd = self.ihelper.cwd()
    self.assertNotEqual(cwd, None)
    self.assertEqual(type(cwd), str)

  def test_get_root(self):
    "Get the root directory from the helper"
    self.ihelper = ih.IrodsHelper()
    self.assertNotEqual(self.ihelper, None)
    root = self.ihelper.root()
    self.assertNotEqual(root, None)
    self.assertEqual(type(root), str)

  def test_cwd_is_root(self):
    "The initial working directory should be the root directory"
    self.ihelper = ih.IrodsHelper()
    self.assertNotEqual(self.ihelper, None)
    root = self.ihelper.root()
    cwd = self.ihelper.cwd()
    self.assertEqual(cwd, root)


class MovementTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = ih.IrodsHelper()          # create instance of class under test
    self.assertTrue(self.ihelper.is_connected())

  def tearDown(self):
    "Cleanup the test case"
    self.ihelper.disconnect()


  def test_set_root(self):
    "Reset the root directory and test root and cwd"
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.assertEqual(cwd1, root1)
    self.ihelper.set_root()                  # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    self.assertEqual(cwd2, root2)
    self.assertEqual(cwd1, cwd2)
    self.assertEqual(root1, root2)

  def test_set_root2(self):
    "Reset the root directory and test root and cwd"
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.assertEqual(cwd1, root1)
    self.ihelper.set_root(top_dir="analyses") # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    self.assertNotEqual(root1, root2)
    self.assertNotEqual(cwd1, cwd2)
    self.assertEqual(cwd2, root2)

  def test_cd_down(self):
    "Move down in the filesystem tree"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.assertEqual(cwd1, root1)
    self.ihelper.cd_down("test")            # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    self.assertNotEqual(cwd2, root2)        # cwd changed from root

  def test_cd_down2(self):
    "Move down further in the filesystem tree"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.assertEqual(cwd1, root1)
    self.ihelper.cd_down("test/tstsubdir")  # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    self.assertNotEqual(cwd2, root2)        # cwd changed from root

  def test_cd_root_at_home(self):
    "Calling cd_root at user home does nothing"
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.ihelper.cd_root()                  # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertEqual(cwd1, cwd2)            # cwd should be unchanged

  def test_cd_root(self):
    "Move back to user home in the filesystem tree"
    self.ihelper.cd_down("xxx/yyy")         # "move down" in tree
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.assertNotEqual(cwd1, root1)        # cwd now moved from root
    self.ihelper.cd_root()                  # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    self.assertEqual(root2, root1)          # root should be unchanged
    self.assertEqual(cwd2, root1)           # cwd returned to same as root


  def test_cd_rel_down1(self):
    "From subdir move down one dir in the filesystem tree, relative to the cwd"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    self.ihelper.cd_down("testDir")         # cwd down from root
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    # print("\n{}, {}".format(root1, cwd1))
    self.assertNotEqual(cwd1, root1)
    self.ihelper.cd("test0")                # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    endcwd = "{}/{}/{}".format(root1, "testDir", "test0")
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_rel_down1_fromroot(self):
    "Move down one dir in the filesystem tree, relative to cwd=root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()               # cwd same as root
    testdir = "test"
    # print("\n{}, {}".format(root1, cwd1))
    self.assertEqual(cwd1, root1)
    self.ihelper.cd(testdir)                 # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    endcwd = "{}/{}".format(root1, testdir)
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_rel_downN(self):
    "Move down multiple dirs in the filesystem tree, relative to the cwd"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    self.ihelper.cd_down("testDir")         # cwd down from root
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    # print("\n{}, {}".format(root1, cwd1))
    self.assertNotEqual(cwd1, root1)
    self.ihelper.cd("test0/test1/test3")    # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    endcwd = "{}/{}/{}".format(root1, "testDir", "test0/test1/test3")
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_rel_downN_fromroot(self):
    "Move down multiple dirs in the filesystem tree, relative to cwd=root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()               # cwd same as root
    # print("\n{}, {}".format(root1, cwd1))
    self.assertEqual(cwd1, root1)
    self.ihelper.cd("test0/test1/test3")    # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    endcwd = "{}/{}".format(root1,"test0/test1/test3") # the test call
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_rel_uptoroot(self):
    "Move relative should not be able to rise above the root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    self.ihelper.set_root(top_dir=self.root_dir) # cwd and root set down from root
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    # print("\n{}, {}".format(root1, cwd1))
    self.assertEqual(cwd1, root1)
    self.ihelper.cd("/iplant/home")         # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertEqual(cwd1, cwd2)            # cwd NOT changed from previous
    self.assertEqual(cwd2, root1)           # cwd where it should be at end


  def test_cd_abs_down1(self):
    "From subdir move down one dir in the filesystem tree, relative to the root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    self.ihelper.cd("testDir")              # cwd down from root
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    # print("\n{}, {}".format(root1, cwd1))
    self.assertNotEqual(cwd1, root1)
    self.ihelper.cd("test0", absolute=True) # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    endcwd = "{}/{}".format(root1, "test0")
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_abs_down1_fromroot(self):
    "Move down one dir in the filesystem tree, relative to cwd=root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()               # cwd same as root
    # print("\n{}, {}".format(root1, cwd1))
    self.assertEqual(cwd1, root1)
    self.ihelper.cd("test", absolute=True)  # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    self.assertNotEqual(cwd2, root2)        # cwd changed from root
    endcwd = "{}/{}".format(root1, "test")
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_abs_downN(self):
    "Move down multiple dirs in the filesystem tree, relative to the root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    self.ihelper.cd_down("testDir")         # cwd down from root
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    # print("\n{}, {}".format(root1, cwd1))
    self.assertNotEqual(cwd1, root1)
    self.ihelper.cd("test0/test1/test3", absolute=True)  # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    endcwd = "{}/{}".format(root1, "test0/test1/test3")
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_abs_downN_fromroot(self):
    "Move down multiple dirs in the filesystem tree, relative to cwd=root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()               # cwd same as root
    # print("\n{}, {}".format(root1, cwd1))
    self.assertEqual(cwd1, root1)
    self.ihelper.cd("test0/test1/test3", absolute=True) # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertNotEqual(cwd1, cwd2)         # cwd changed from previous
    self.assertNotEqual(cwd2, root2)        # cwd changed from root
    endcwd = "{}/{}".format(root1,"test0/test1/test3") # the test call
    self.assertEqual(cwd2, endcwd)          # cwd where it should be at end

  def test_cd_abs_uptoroot(self):
    "Move absolute should not be able to rise above the root"
    # NB: CWD state is internal to the helper class and is not checked against the
    #     iRods filesystem for validity.
    self.ihelper.set_root(top_dir=self.root_dir) # cwd and root set down from root
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    # print("\n{}, {}".format(root1, cwd1))
    self.assertEqual(cwd1, root1)
    self.ihelper.cd("/iplant/home", absolute=True)  # the test call
    root2 = self.ihelper.root()
    cwd2 = self.ihelper.cwd()
    # print("{}, {}".format(root2, cwd2))
    self.assertEqual(root1, root2)          # root should be unchanged
    self.assertEqual(cwd1, cwd2)            # cwd NOT changed from previous
    self.assertEqual(cwd2, root1)           # cwd where it should be at end


class FilesTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = ih.IrodsHelper()          # create instance of class under test
    self.assertTrue(self.ihelper.is_connected())

  def tearDown(self):
    "Cleanup the test case"
    self.ihelper.cd_root()                   # reset root
    # self.ihelper.delete_file("context.py")
    # self.ihelper.delete_file("empty.txt")
    # self.ihelper.delete_dir("testDir", force=True)
    # self.ihelper.delete_dir("test", force=True)
    self.ihelper.disconnect()


  def test_mkdir(self):
    "Make a new directory and move into it"
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.assertEqual(cwd1, root1)
    id = self.ihelper.mkdir("testDir")       # the test call
    self.ihelper.cd_down("testDir")          # move into new subdir
    cwd2 = self.ihelper.cwd()
    self.assertNotEqual(cwd1, cwd2)

  def test_mkdir2(self):
    "Make multiple new directories and move to the bottom one"
    root1 = self.ihelper.root()
    cwd1 = self.ihelper.cwd()
    self.assertEqual(cwd1, root1)
    id = self.ihelper.mkdir("testDir/test/tmp") # the test call
    self.ihelper.cd_down("testDir/test/tmp")    # move into new subdir
    cwd2 = self.ihelper.cwd()
    self.assertNotEqual(cwd1, cwd2)


  def test_getf_bad_file_rel(self):
    "Throws exception on bad relative filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.ihelper.getf("BAD_FILENAME")

  def test_getf_bad_file_abs(self):
    "Throws exception on bad absolute filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.ihelper.getf("BAD_FILENAME", True)

  def test_get_dir_bad_dir_rel(self):
    "Throws exception on bad relative dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.ihelper.get_dir("BAD_DIRNAME")

  def test_get_dir_bad_dir_abs(self):
    "Throws exception on bad absolute dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.ihelper.get_dir("BAD_DIRNAME", True)


  def test_get_cwd(self):
    """ Get dir info for the current working directory. """
    pwd = self.ihelper.cwd()
    dobj = self.ihelper.get_cwd()            # the test call
    self.assertNotEqual(dobj, None)
    self.assertEqual(dobj.path, pwd)

  def test_get_cwd_subdir(self):
    """ Get dir info for a subdirectory. """
    dirpath = "testDir"
    self.ihelper.mkdir(dirpath)
    self.ihelper.cd_down(dirpath)
    pwd = self.ihelper.cwd()
    dobj = self.ihelper.get_cwd()            # the test call
    self.assertNotEqual(dobj, None)
    self.assertEqual(dobj.name, dirpath)
    self.assertEqual(dobj.path, pwd)

  def test_get_root(self):
    """ Get dir info for the users root directory. """
    root = self.ihelper.root()
    dobj = self.ihelper.get_root()            # the test call
    self.assertNotEqual(dobj, None)
    self.assertEqual(dobj.path, root)


  def test_put_file_empty(self):
    "Upload an empty file to users home directory"
    upfile = "empty.txt"
    self.ihelper.put_file(upfile, upfile)    # the test call
    obj = self.ihelper.getf(upfile)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, upfile)

  def test_put_file_basic(self):
    "Upload a test file to users home directory"
    upfile = "context.py"
    self.ihelper.put_file(upfile, upfile)    # the test call
    obj = self.ihelper.getf(upfile)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, upfile)

  def test_put_file_2nest_cd(self):
    "Upload a test file to a newly created nested directory after cd"
    upfile = "context.py"
    dirpath = "testDir/test2"
    self.ihelper.mkdir(dirpath)
    self.ihelper.cd_down(dirpath)
    self.ihelper.put_file(upfile, upfile)    # the test call
    obj = self.ihelper.getf(upfile)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, upfile)

  def test_put_file_2nest_nocd(self):
    "Upload a test file directly to a newly created nested directory"
    upfile = "context.py"
    dirpath = "testDir/test2"
    filepath = "{}/{}".format(dirpath, upfile)
    self.ihelper.mkdir(dirpath)
    self.ihelper.put_file(upfile, filepath)  # the test call
    obj = self.ihelper.getf(filepath, absolute=True)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, upfile)

  def test_put_file_rename(self):
    "Upload a file to iRods home directory with a new name"
    upfile = "empty.txt"
    newname = "still_empty.txt"
    basefile = os.path.basename(upfile)
    self.ihelper.put_file(upfile, newname)   # the test call
    obj = self.ihelper.getf(newname)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, newname)

  def test_put_file_nest2home(self):
    "Upload a nested file to iRods home directory"
    upfile = "resources/empty2.txt"
    basefile = os.path.basename(upfile)
    self.ihelper.put_file(upfile, basefile)  # the test call
    obj = self.ihelper.getf(basefile)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, basefile)

  def test_put_file_nest2nest(self):
    "Upload a nested file to a relative nested path"
    upfile = "resources/empty2.txt"
    basefile = os.path.basename(upfile)
    dirpath = "testDir/test2"
    filepath = "{}/{}".format(dirpath, basefile)
    self.ihelper.mkdir(dirpath)
    self.ihelper.put_file(upfile, filepath)  # the test call
    obj = self.ihelper.getf(filepath)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, basefile)

  def test_put_file_nest2nest_rename(self):
    "Upload a nested file to a relative nested path with rename"
    upfile = "resources/empty2.txt"
    newname = "empty2_copy.txt"
    dirpath = "testDir/test2"
    filepath = "{}/{}".format(dirpath, newname)
    self.ihelper.mkdir(dirpath)
    self.ihelper.put_file(upfile, filepath)  # the test call
    obj = self.ihelper.getf(filepath)
    self.assertNotEqual(obj, None)
    self.assertEqual(obj.name, newname)


  def test_get_metac_bad_dir_rel(self):
    "Throws exception on bad relative dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.ihelper.get_metac("BAD_DIRNAME")

  def test_get_metac_bad_dir_abs(self):
    "Throws exception on bad absolute dirpath"
    with self.assertRaises(CollectionDoesNotExist):
      self.ihelper.get_metac("BAD_DIRNAME", True)

  def test_get_metac(self):
    "Make a directory and then get metadata for it"
    dirpath = "testDir"
    self.ihelper.mkdir(dirpath)
    md = self.ihelper.get_metac(dirpath)
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)

  def test_get_metaf_bad_file_rel(self):
    "Throws exception on bad relative filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.ihelper.get_metaf("BAD_FILENAME")

  def test_get_metaf_bad_file_abs(self):
    "Throws exception on bad absolute filepath"
    with self.assertRaises(DataObjectDoesNotExist):
      self.ihelper.get_metaf("BAD_FILENAME", True)

  def test_get_metaf_abs(self):
    "Put a file and then get metadata for it using absolute path"
    dirpath = "testDir"
    upfile = "context.py"
    filepath = "{}/{}".format(dirpath, upfile)
    self.ihelper.mkdir(dirpath)
    self.ihelper.put_file(upfile, filepath)
    md = self.ihelper.get_metaf(filepath, absolute=True) # the test call
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)

  def test_get_metaf_rel(self):
    "Put a file and then get metadata for it using relative path"
    dirpath = "testDir"
    upfile = "context.py"
    self.ihelper.mkdir(dirpath)
    self.ihelper.cd_down(dirpath)
    self.ihelper.put_file(upfile, upfile)
    md = self.ihelper.get_metaf(upfile)    # the test call
    self.assertNotEqual(md, None)
    self.assertEqual(type(md), list)
    self.assertTrue(len(md) > 0)


  def test_put_metaf_bad_file_rel(self):
    "Throws exception on bad relative filepath"
    mdata = [("Key1", "Value1")]
    with self.assertRaises(DataObjectDoesNotExist):
      self.ihelper.put_metaf(mdata, "BAD_FILENAME") # the test call

  def test_put_metaf_bad_file_abs(self):
    "Throws exception on bad absolute filepath"
    mdata = [("Key1", "Value1")]
    with self.assertRaises(DataObjectDoesNotExist):
      self.ihelper.put_metaf(mdata, "BAD_FILENAME", True) # the test call

  def test_put_metaf_none(self):
    "Create a file and then put empty metadata on it"
    dirpath = "testDir"
    upfile = "empty.txt"
    mdata = []
    self.ihelper.mkdir(dirpath)
    self.ihelper.cd_down(dirpath)
    self.ihelper.put_file(upfile, upfile)
    md0 = self.ihelper.get_metaf(upfile)
    self.assertNotEqual(md0, None)
    self.assertEqual(type(md0), list)
    # print("\nMD0=", *md0, sep="\n")

    cnt1 = self.ihelper.put_metaf(mdata, upfile) # the test call
    md1 = self.ihelper.get_metaf(upfile)
    # print("\nMD1=", *md1, sep="\n")
    self.assertNotEqual(md1, None)
    self.assertEqual(type(md1), list)
    self.assertTrue(len(md1) > len(mdata))
    self.assertEqual(len(md0), len(md1))
    self.assertEqual(len(md0), cnt1)

  def test_put_metaf_rel(self):
    "Create a file and then put metadata on it using a relative path"
    dirpath = "testDir"
    upfile = "context.py"
    mdata = [ Metadatum("Key1", "Value1"), Metadatum("KEY2", "VALUE2"),
              Metadatum("BIG_KEY3", "Three of Hearts") ]
    mdata2 = [ Metadatum("Key1", "NewValue1"), Metadatum("KEY2", "NEW_VALUE2"),
               Metadatum("BIG_KEY3", "NO TRUMP") ]
    self.ihelper.mkdir(dirpath)
    self.ihelper.cd_down(dirpath)
    self.ihelper.put_file(upfile, upfile)
    md0 = self.ihelper.get_metaf(upfile)
    # print("\nMD0=", *md0, sep="\n")

    cnt1 = self.ihelper.put_metaf(mdata, upfile) # the test call
    md1 = self.ihelper.get_metaf(upfile)
    # print("\nMD1=", *md1, sep="\n")
    self.assertNotEqual(md1, None)
    self.assertEqual(type(md1), list)
    self.assertTrue(len(md1) > len(mdata))
    self.assertEqual(len(md1), cnt1)

    cnt2 = self.ihelper.put_metaf(mdata2, upfile) # the test call
    md2 = self.ihelper.get_metaf(upfile)
    # print("\nMD2=", *md2, sep="\n")
    self.assertNotEqual(md2, None)
    self.assertEqual(type(md2), list)
    self.assertTrue(len(md2) > len(mdata2))
    self.assertNotEqual(md1, md2)
    self.assertEqual(len(md1), len(md2))
    self.assertEqual(len(md2), cnt2)

  def test_put_metaf_abs(self):
    "Create a file and then put metadata on it using an absolute path"
    dirpath = "testDir/test"
    upfile = "context.py"
    filepath = "{}/{}".format(dirpath, upfile)
    mdata = [ Metadatum("Key1", "Value1"), Metadatum("KEY2", "VALUE2"),
              Metadatum("BIG_KEY3", "Three of Hearts") ]
    mdata2 = [ Metadatum("Key1", "NewValue1"), Metadatum("KEY2", "NEW_VALUE2"),
               Metadatum("BIG_KEY3", "NO TRUMP") ]
    self.ihelper.cd_root()
    self.ihelper.mkdir(dirpath)
    self.ihelper.put_file(upfile, filepath)
    md0 = self.ihelper.get_metaf(filepath, absolute=True)
    # print("\nMD0=", *md0, sep="\n")

    cnt1 = self.ihelper.put_metaf(mdata, filepath, absolute=True) # the test call
    md1 = self.ihelper.get_metaf(filepath, absolute=True)
    # print("\nMD1=", *md1, sep="\n")
    self.assertNotEqual(md1, None)
    self.assertEqual(type(md1), list)
    self.assertTrue(len(md1) > len(mdata))
    self.assertEqual(len(md1), cnt1)

    cnt2 = self.ihelper.put_metaf(mdata2, filepath, absolute=True) # the test call
    md2 = self.ihelper.get_metaf(filepath, absolute=True)
    # print("\nMD2=", *md2, sep="\n")
    self.assertNotEqual(md2, None)
    self.assertEqual(type(md2), list)
    self.assertTrue(len(md2) > len(mdata2))
    self.assertNotEqual(md1, md2)
    self.assertEqual(len(md2), cnt2)

  def test_put_metaf_multi(self):
    "Create a file and then replace old and put new metadata on it"
    dirpath = "testDir"
    upfile = "empty.txt"
    mdata = [ Metadatum("Key1", "Value1"), Metadatum("KEY2", "Value2"),
              Metadatum("KEY2", "Two Many") ]
    mdata2 = [ Metadatum("Key1", "NewVal1"), Metadatum("KEY2", "Only2"),
               Metadatum("KEY3", "333"), Metadatum("KEY3", "THREE") ]
    self.ihelper.mkdir(dirpath)
    self.ihelper.cd_down(dirpath)
    self.ihelper.put_file(upfile, upfile)
    md0 = self.ihelper.get_metaf(upfile)
    # print("\nMD0=", *md0, sep="\n")

    cnt1 = self.ihelper.put_metaf(mdata, upfile) # the test call
    md1 = self.ihelper.get_metaf(upfile)
    # print("\nMD1=", *md1, sep="\n")
    self.assertNotEqual(md1, None)
    self.assertEqual(type(md1), list)
    self.assertTrue(len(md1) > len(mdata))
    self.assertEqual(len(md1), cnt1)

    cnt2 = self.ihelper.put_metaf(mdata2, upfile) # the test call
    md2 = self.ihelper.get_metaf(upfile)
    # print("\nMD2=", *md2, sep="\n")
    self.assertNotEqual(md2, None)
    self.assertEqual(type(md2), list)
    self.assertTrue(len(md2) > len(mdata2))
    self.assertNotEqual(md1, md2)
    self.assertEqual(len(md2), cnt2)


class WalkTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = ih.IrodsHelper()          # create instance of class under test
    self.assertTrue(self.ihelper.is_connected()) # sanity check: assert connected
    upfile = "context.py"                 # build a test directory tree
    upfile2 = "metadata-keys.txt"
    self.ihelper.mkdir("test0/test1/test3")
    self.ihelper.mkdir("test0/test1/test4")
    self.ihelper.mkdir("test0/test2/test5")
    self.ihelper.put_file(upfile, "test0/test1/" + upfile)
    self.ihelper.put_file(upfile, "test0/test1/test3/" + upfile)
    self.ihelper.put_file(upfile, "test0/test2/test5/" + upfile)
    self.ihelper.put_file(upfile2, "test0/test2/test5/" + upfile2)
    self.ihelper.cd_down("test0")

  def tearDown(self):
    "Cleanup the test case"
    self.ihelper.disconnect()


  def test_walk_topdown(self):
    """ Walk a directory tree in top-down order. """
    walker = self.ihelper.walk()             # the test call

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
    walker = self.ihelper.walk(topdown=False) # the test call

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


class DeleteTestCase(IrodsHelpTestCase):

  def setUp(self):
    "Initialize the test case"
    self.ihelper = ih.IrodsHelper()          # create instance of class under test
    self.assertTrue(self.ihelper.is_connected()) # sanity check: assert connected

  def test_delete_files(self):
    "Create and delete files in directories and subdirectories. WARNING: test takes forever!"
    upfile1 = "context.py"
    upfile2 = "empty.txt"
    testdir = "testDir"
    testdir2 = "test/test1/test"
    self.ihelper.mkdir(testdir)
    self.ihelper.mkdir(testdir2)
    self.ihelper.put_file(upfile1, upfile1)
    self.ihelper.put_file(upfile2, upfile2)
    self.ihelper.put_file(upfile1, "{}/{}".format(testdir, upfile1))
    self.ihelper.put_file(upfile2, "{}/{}".format(testdir, upfile2))
    self.ihelper.put_file(upfile1, "{}/{}".format(testdir2, upfile1))

    self.assertTrue(self.ihelper.delete_file(upfile1))
    self.assertTrue(self.ihelper.delete_file(upfile2))
    self.assertTrue(self.ihelper.delete_file("{}/{}".format(testdir, upfile1)))
    self.assertTrue(self.ihelper.delete_file("{}/{}".format(testdir, upfile2)))
    self.assertTrue(self.ihelper.delete_file("{}/{}".format(testdir2, upfile1)))

  def test_delete_dirs(self):
    "Create and delete directories and subdirectories. WARNING: test takes forever!"
    testdirs = [
      "testDir",
      "test/test1/test2/test4",
      "test/test1/test2",
      "test/test1",
      "test",
    ]
    for td in testdirs:
      self.ihelper.mkdir(td)
    deletes = [self.ihelper.delete_dir(td) for td in testdirs]
    self.assertTrue(all(deletes))

  def test_delete_dirs_recurse(self):
    "Delete directories works recursively. WARNING: test takes forever!"
    testdirs = [
      "test",
      "test/test1/test2/test4"
    ]
    for td in testdirs:
      self.ihelper.mkdir(td)
    deletes = [self.ihelper.delete_dir(td) for td in testdirs]
    self.assertTrue(deletes[0])             # delete is recursive
    self.assertFalse(deletes[1])            # so it is too late for this call


if __name__ == "__main__":
  suite = suite()
  unittest.TextTestRunner(verbosity=2).run(suite)
