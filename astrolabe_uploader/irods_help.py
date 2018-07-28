"""
Helper class for iRods commands: manipulate the filesystem, including metadata.
  Last Modified: Make imports absolute.
"""
import os
import logging
import pathlib as pl
from irods.session import iRODSSession
from astrolabe_uploader import Metadatum

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


    def __init__(self, options={}, connect=True):
        self._cwdpath = None                # current working directory - a PurePath
        self._root = None                   # root directory path - a PurePath
        self._session = None                # current session
        self._options = options             # dict of settings for this class
        if (connect):                       # connect now unless specified otherwise
            self.connect()

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

    def connect(self):
        """ Create an iRods session using the instantiation options, or
            a file specified by the environment variable IRODS_ENVIRONMENT_FILE, or
            the default irods_environment.json file.
        """
        logging.info("(IrodsHelper.connect): options={}".format(self._options))
        try:
            env_file = self._options["irods_env_file"]
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
        """ Return the current working directory path as a string. """
        return str(self._cwdpath)

    def delete_dir(self, dir_path, absolute=False, force=False, recurse=True):
        """ Delete the specified directory relative to the iRods current working directory
            (default) OR relative to the users root directory, if the absolute argument is True.
        """
        try:
            dirobj = self.getc(dir_path, absolute=absolute)
            dirobj.remove(force=force, recurse=recurse)
            return True
        except:                             # ignore any errors
            return False

    def delete_file(self, file_path, absolute=False):
        """ Delete the specified file relative to the iRods current working directory (default)
            OR relative to the users root directory, if the absolute argument is True.
        """
        try:
            obj = self.getf(file_path, absolute=absolute)
            obj.unlink(force=True)
            return True
        except:                             # ignore any errors
            return False

    def disconnect(self):
        """ Close down and cleanup the current session. """
        logging.info("(IrodsHelper.disconnect)")
        if (self._session):
            self._session.cleanup()
            self._session = None

    def getc(self, dir_path, absolute=False):
        """ Get the specified directory relative to the iRods current working directory (default)
            OR relative to the users root directory, if the absolute argument is True.
        """
        if (absolute):
            dirpath = self.abs_path(dir_path) # path is relative to root dir
        else:
            dirpath = self.rel_path(dir_path) # path is relative to current working dir
        return self._session.collections.get(dirpath)

    def get_cwd(self):
        """ Get directory information for the current working directory. """
        return self._session.collections.get(self._cwdpath) if (self._cwdpath) else None

    def getf(self, file_path, absolute=False):
        """ Get the specified file relative to the iRods current working directory (default)
            OR relative to the users root directory, if the absolute argument is True.
        """
        if (absolute):
            filepath = self.abs_path(file_path) # path is relative to root dir
        else:
            filepath = self.rel_path(file_path) # path is relative to current working dir
        return self._session.data_objects.get(filepath)

    def get_metac(self, dir_path, absolute=False):
        """ Get the metadata for the specified directory relative to the iRods
            current working directory (default) OR relative to the users root directory,
            if the absolute argument is True.
        """
        dirobj = self.getc(dir_path, absolute=absolute)
        return [Metadatum(item.name, item.value) for item in dirobj.metadata.items()]

    def get_metaf(self, file_path, absolute=False):
        """ Get the metadata for the specified file relative to the iRods
            current working directory (default) OR relative to the users root directory,
            if the absolute argument is True.
        """
        obj = self.getf(file_path, absolute=absolute)
        return [Metadatum(item.name, item.value) for item in obj.metadata.items()]

    def get_root(self):
        """ Get directory information for the users root directory. """
        return self._session.collections.get(self._root)

    def mkdir(self, subdir_name):
        """ Make a directory (collection) with the given name at the current working directory.
            Returns the iRods ID of the collection.
        """
        return self._session.collections.create(self.rel_path(subdir_name))

    def put_file(self, local_file, file_path, absolute=False):
        """ Upload the specified local file to the specified path, relative to the iRods
            current working directory (default) OR relative to the users root directory,
            if the absolute argument is True.
        """
        if (absolute):
            filepath = self.abs_path(file_path) # path is relative to root dir
        else:
            filepath = self.rel_path(file_path) # path is relative to current working dir
        self._session.data_objects.put(local_file, filepath)

    def put_metaf(self, metadata, file_path, absolute=False):
        """ Attach the given metadata on the file specified relative to the iRods
            current working directory (default) OR relative to the users root directory,
            if the absolute argument is True. Returns the new number of metadata items.
        """
        obj = self.getf(file_path, absolute=absolute)
        keys = [item.keyword for item in metadata]
        for key in keys:
            del(obj.metadata[key])
        for item in metadata:
            obj.metadata.add(item.keyword, item.value)
        return len(obj.metadata)

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
        self.set_root()                     # call with default arguments

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

    def walk(self, topdown=True):
        """ Collection tree generator. For each subcollection in the dir tree,
            starting at the current working directory, yield a 3-tuple of
            (self, self.subcollections, self.data_objects)
        """
        cwd = self.get_cwd()
        if (cwd):
            yield from cwd.walk(topdown=topdown)
