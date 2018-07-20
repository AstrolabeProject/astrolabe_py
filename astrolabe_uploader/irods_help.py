"""
Helper class for iRods commands: manipulate the filesystem, including metadata.
  Last Modified: Mkdir returns iRods ID. Add put. Rename method to cd_root.
"""
__version__ = "0.0.2"
__author__ = "Tom Hicks"

import os
import logging
import pathlib as pl
from irods.session import iRODSSession

logging.basicConfig(level=logging.ERROR)    # default logging configuration

class IrodsHelper:
    """ Helper class for iRods commands """

    _CWD_FORMAT = "/{}/{}/{}"

    @staticmethod
    def make_session(**kwargs):
        """ Create and return an iRods session using the given keyword arguments. """
        try:
            env_file = kwargs["irods_env_file"]
        except KeyError:
            try:
                env_file = os.environ["IRODS_ENVIRONMENT_FILE"]
            except KeyError:
                env_file = os.path.expanduser("~/.irods/irods_environment.json")
        return iRODSSession(irods_authentication_uid=uid, irods_env_file=env_file)

    @staticmethod
    def cleanup_session(session):
        """ Cleanup the given session. """
        if (session):
            session.cleanup()


    def __init__(self):
        self._cwdpath = None                # current working directory path
        self._root = None                   # root directory path
        self._session = None                # current session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()


    def cleanup(self):
        """ Cleanup the current session. """
        self.disconnect()

    def connect(self, options):
        """ Create an iRods session using the given options, or
            a file specified by the environment variable IRODS_ENVIRONMENT_FILE, or
            the default irods_environment.json file.
        """
        logging.info("(IrodsHelper.connect): options={}".format(options))
        try:
            env_file = options["irods_env_file"]
        except KeyError:
            try:
                env_file = os.environ["IRODS_ENVIRONMENT_FILE"]
            except KeyError:
                env_file = os.path.expanduser("~/.irods/irods_environment.json")

        logging.info("IrodsHelper.connect: env_file={}".format(env_file))

        self._session = iRODSSession(irods_env_file=env_file)
        logging.info("IrodsHelper.connect: SESSION={}".format(self._session))

        self.set_root()
        logging.info("IrodsHelper.connect:    ROOT={}".format(self._root))
        logging.info("IrodsHelper.connect: CWDPATH={}".format(self._cwdpath))

    def is_connected(self):
        """ Tell whether this class is currently connected to iRods. """
        return (bool(self._session))

    def cd_down(self, subdir):
        """ Change the current working directory to the given subdirectory. """
        if (self._cwdpath):
            self._cwdpath = self._cwdpath / subdir

    def cd_root(self):
        """ Reset the current working directory to the users top-level directory. """
        if (self._root):
            self._cwdpath = pl.PurePath(self._root)
        else:
            self._cwdpath = None

    def cd_up(self):
        """ Change the current working directory to the parent directory. """
        if (self._cwdpath and self._root):
            parent = self._cwdpath.parent
            if (parent >= self._root):      # must not rise above root dir
                self._cwdpath = parent
        else:
            self._cwdpath = None

    def cwd(self):
        """ Return the current working directory as a string. """
        return str(self._cwdpath)

    def disconnect(self, options=None):
        """ Close down and cleanup the current session. """
        logging.info("(IrodsHelper.disconnect)")
        if (self._session):
            self._session.cleanup()
            self._session = None

    def mkdir(self, subdir_name):
        """ Make a directory (collection) with the given name at the current working directory.
            Returns the iRods ID of the collection.
        """
        return self._session.collections.create(self._cwdpath / subdir_name)

    def put(self, file_path):
        """ Upload the specified local file to the iRods current working directory. """
        self._session.data_objects.put(file_path, self._cwdpath)

    def root(self):
        """ Return the user root directory as a string. """
        return str(self._root)

    def session(self):
        """ Return the current session object. """
        return self._session

    def set_connection(self, json_body):
        """ Create a session and set it as current, using the fields of the given JSON object. """
        self.disconnect()                   # close and cleanup any existing session
        self._session = iRODSSession(
            host=json_body["host"],
            port=json_body["port"],
            user=json_body["user"],
            password=json_body["password"],
            zone=json_body["zone"])
        self.set_root()                     # call with empty options

    def set_root(self, home_dir="home", top_dir=""):
        """ Compute and set the root directory path to the users iRods home directory. """
        if (self._session):
            self._root = pl.PurePath("/", self._session.zone, home_dir, self._session.username, top_dir)
        else:
            self._root = None
        self.cd_root()                      # reset home after changing root dir
