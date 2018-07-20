"""
Helper class for iRods commands: manipulate the filesystem, including metadata.
  Last Modified: Mkdir returns iRods ID. Add put. Rename cd_root. Workout abs/rel path logic.
"""
__version__ = "0.0.4"
__author__ = "Tom Hicks"

import os
import logging
import pathlib as pl
from irods.session import iRODSSession

logging.basicConfig(level=logging.INFO)    # default logging configuration

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
        self._cwdpath = None                # current working directory - a PurePath
        self._root = None                   # root directory path - a PurePath
        self._session = None                # current session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()


    def abs_path(self, path):
        """ Return an iRods path for the given path relative to the users root directory. """
        return str(self._root / path)

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
            self._cwdpath = self._cwdpath / subdir # NB: maintain PurePath

    def cd_root(self):
        """ Reset the current working directory to the users root directory. """
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

    def get(self, file_path, absolute=False):
        """ Get the specified local file relative to the iRods current working directory (default)
            OR relative to the users root directory, if the absolute argument is True.
        """
        if (absolute):
            filepath = self.abs_path(file_path) # path is relative to root dir
        else:
            filepath = self.rel_path(file_path) # path is relative to current working dir
        return self._session.data_objects.get(filepath)

    def mkdir(self, subdir_name):
        """ Make a directory (collection) with the given name at the current working directory.
            Returns the iRods ID of the collection.
        """
        return self._session.collections.create(self.rel_path(subdir_name))

    def put(self, local_file, to_dir=None):
        """ Upload the specified local file to the iRods current working directory (default) or
            to a directory specified by the 'to_dir' argument.
        """
        target_dir = self.cwd()                # default is the current working directory
        if (to_dir):                           # if alternate directory path specified
            target_dir = self.abs_path(to_dir) # then dir path is relative to users root dir
        self._session.data_objects.put(local_file, self.to_dirpath(target_dir))

    def rel_path(self, path):
        """ Return an iRods path for the given path relative to the current working directory. """
        return str(self._cwdpath / path)

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
        """ Compute and set the users root directory to the users iRods home directory (default)
            OR to a subdirectory of the users home directory, specified by the 'top_dir' argument.
        """
        if (self._session):
            self._root = pl.PurePath("/", self._session.zone, home_dir, self._session.username, top_dir)
        else:
            self._root = None
        self.cd_root()                      # cd back to root after changing root dir

    def to_dirpath(self, dir_path):
        """ Add a trailing slash to the given directory path to mark it is an iRods
            directory path. This is required by the 'put' command, for example. """
        if (str(dir_path).endswith("/")):
            return str(dir_path)
        else:
            return "{}/".format(dir_path)
