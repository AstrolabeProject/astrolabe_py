"""
Module to manipulate file metadata.
  Last Modified: Fix instance variables. Use double quotes, module dunders. Mark statics. Remove unused methods.
"""
__version__ = "0.0.1"
__author__ = "Tom Hicks"

import os
import logging
from irods.session import iRODSSession

logging.basicConfig(level=logging.ERROR) # default logging configuration

class IrodsHelper:
    """ Helper class for iRods commands """

    _CWD_FORMAT = "/{}/home/{}"

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
        self._cwd = None                    # current working directory
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
            self.cd_home()
            logging.info("IrodsHelper.connect: CWD={}".format(self._cwd))

    def is_connected(self):
        """ Tell whether this class is currently connected to iRods. """
        return (bool(self._session))

    def cd_down(self, subdir):
        """ Change the current working directory to the given subdirectory. """
        if (self._session):
            pass                            # TODO: IMPLEMENT LATER
        else:
            self._cwd = None

    def cd_home(self):
        """ Reset the current working directory to the users home directory. """
        if (self._session):
            self._cwd = self._CWD_FORMAT.format(self._session.zone,self._session.username)
        else:
            self._cwd = None

    def cd_up(self):
        """ Change the current working directory to the parent directory. """
        if (self._session):
            pass                            # TODO: IMPLEMENT LATER
        else:
            self._cwd = None

    def cwd(self):
        """ Return the current working directory. """
        return self._cwd

    def disconnect(self, options=None):
        """ Close down and cleanup the current session. """
        logging.info("(IrodsHelper.disconnect)")
        if (self._session):
            self._session.cleanup()
            self._session = None

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
        self.cd_home()
