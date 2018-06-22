# #!/usr/bin/env python3
#
# Python code to (unit) test the Astrolabe Data Stores iRods module.
#   Written by: Tom Hicks. 6/21/2018.
#   Last Modified: Initial creation.
#
from astrolabe_data_stores import irods
import unittest

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ListTestCase))
  return suite


class IrodsTestCase(unittest.TestCase):

  "Base Irods class"
  @classmethod
  def setUpClass(cls):
    datalab = irods.Irods()
    cls.dl = datalab


class OptionTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.option = irods.Option(self.dl)


class TaskTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.task = irods.Task(self.dl)


class LoginTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.login = irods.Login(self.dl)


class LogoutTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.logout = irods.Logout(self.dl)


class AddCapabilityTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.addCapability = irods.AddCapability(self.dl)


class ListCapabilityTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.listCapability = irods.ListCapability(self.dl)


class QueryTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.query = irods.Query(self.dl)


class LaunchJobTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.launchjob = irods.LaunchJob(self.dl)


class MountvofsTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.mountvofs = irods.Mountvofs(self.dl)


class PutTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.put = irods.Put(self.dl)


class GetTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.get = irods.Get(self.dl)


class MoveTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.move = irods.Move(self.dl)


class CopyTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.copy = irods.Copy(self.dl)


class DeleteTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.delete = irods.Delete(self.dl)


class LinkTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.link = irods.Link(self.dl)


class ListTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.list = irods.List(self.dl)

  def test_raw(self):
    "Test getting a listing in XML format"
    resp = self.list.run()
    assert

  def test_csv(self):
    "Test getting a listing in CSV format"
    pass

  def test_json(self):
    "Test getting a listing in JSON format"
    pass

  def test_unsupported_format(self):
    "Test getting a listing in an unsupported format"
    pass

  def test_invalid_from(self):
    "Test getting a listing from an invalid location"
    pass


class TagTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.tag = irods.Tag(self.dl)


class MkDirTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.mkdir = irods.MkDir(self.dl)


class RmDirTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.rmdir = irods.RmDir(self.dl)


class ResolveTestCase(IrodsTestCase):

  def setUp(self):
    "Initialize the test case"
    self.resolve = irods.Resolve(self.dl)


if __name__ == '__main__':
  suite = suite()
  unittest.TextTestRunner(verbosity = 2).run(suite)
