"""
Module to manipulate file metadata.
  Written by: Tom Hicks. 6/22/2018.
  Last Modified: Begin to rewrite for Uploader. Use logging.
"""
import os
import logging
from irods.session import iRODSSession

class IrodsHelper:
    """ Helper class for iRods commands """

    logging.basicConfig(level=logging.ERROR) # default logging configuration

    __SESSION__ = None                      # current session

    __CWD_FORMAT__ = "/{}/home/{}"
    __CWD__ = None

    def make_session(**kwargs):
        """ Create and return an iRods session using the given keyword arguments. """
        try:
            env_file = kwargs['irods_env_file']
        except KeyError:
            try:
                env_file = os.environ['IRODS_ENVIRONMENT_FILE']
            except KeyError:
                env_file = os.path.expanduser('~/.irods/irods_environment.json')
        return iRODSSession(irods_authentication_uid=uid, irods_env_file=env_file)

    def cleanup_session(session):
        """ Cleanup the given session. """
        session.cleanup()


    def connect(self, options):
        """ Create an iRods session using the given options, or
            a file specified by the environment variable IRODS_ENVIRONMENT_FILE, or
            the default irods_environment.json file.
        """
        logging.info("TRACE: irods_help.connect")
        try:
            env_file = options['irods_env_file']
        except KeyError:
            try:
                env_file = os.environ['IRODS_ENVIRONMENT_FILE']
            except KeyError:
                env_file = os.path.expanduser('~/.irods/irods_environment.json')

            logging.info("irods_help.connect: env_file={}".format(env_file))
            self.__SESSION__ = iRODSSession(irods_env_file=env_file)
            logging.info("irods_help.connect: SESSION={}".format(self.__SESSION__))
            self.__CWD__ = self.__CWD_FORMAT__.format(self.__SESSION__.zone,self.__SESSION__.username)
            logging.info("irods_help.connect: CWD={}".format(self.__CWD__))

    def is_connected(self):
        """ Tell whether this class is currently connected to iRods. """
        return (bool(self.__SESSION__))

    def cwd(self):
        """ Return the current working directory. """
        return self.__CWD__

    def disconnect(self, options=None):
        """ Disconnect and cleanup the current session. """
        # logging.info("TRACE: irods_help.disconnect")
        if (self.__SESSION__):
            self.__SESSION__.cleanup()
            self.__SESSION__ = None

    def session(self):
        """ Return the current session object. """
        return self.__SESSION__

    def set_connection(self, json_body):
        """ Create a session and set it as current, using the fields of the given JSON object. """
        self.__SESSION__ = iRODSSession(
            host=json_body['host'],
            port=json_body['port'],
            user=json_body['user'],
            password=json_body['password'],
            zone=json_body['zone'])



def test(fits_file, options):
    # logging.info("TRACE: irods_help.test")
    # coll = self.__SESSION__.collections.get("/iplant/home/hickst/sample-data/Hunter/{}".format(fits_file))
    coll = self.__SESSION__.collections.get("/iplant/home/hickst/sample-data/Hunter")
    for obj in coll.data_objects:
        logging.info(obj)
        metadata = obj.metadata.items()
        logging.info("\tMETADATA[" + str(len(metadata)) + "]:")
        for md in metadata:
            logging.info(md)

def save_metadata(fits_file, options, metadata):
    # print("TRACE: irods_help.save_metadata")
    if (self.__SESSION__ is None):
        connect(options)
    logging.info("irods_help.save_metadata: SESSION={}".format(self.__SESSION__))

    # print(str(metadata))
    logging.info("TESTING: {}".format(fits_file))
    test(fits_file, options)
