#
# Module to manipulate file metadata.
#   Written by: Tom Hicks. 6/22/2018.
#   Last Modified: Rewrite for Uploader.
#
import os
from irods.session import iRODSSession

__SESSION__ = None

def connect(options):
    global __SESSION__
    print("TRACE: iRods.connect")
    try:
        env_file = os.environ['IRODS_ENVIRONMENT_FILE']
    except KeyError:
        env_file = os.path.expanduser('~/.irods/irods_environment.json')

    print("iRods.connect: env_file={}".format(env_file))
    __SESSION__ = iRODSSession(irods_env_file=env_file)
    print("iRods.connect: SESSION={}".format(__SESSION__))

def disconnect(options):
    global __SESSION__
    print("TRACE: iRods.disconnect")
    __SESSION__.cleanup()
    __SESSION__ = None

def test(fits_file, options):
    global __SESSION__
    print("TRACE: iRods.test")
    # coll = __SESSION__.collections.get("/iplant/home/hickst/sample-data/Hunter/{}".format(fits_file))
    coll = __SESSION__.collections.get("/iplant/home/hickst/sample-data/Hunter")
    for obj in coll.data_objects:
        print(obj)
        metadata = obj.metadata.items()
        print("\tMETADATA[" + str(len(metadata)) + "]:")
        for md in metadata:
            print(md)

def save_metadata(fits_file, options, metadata):
    global __SESSION__
    print("TRACE: iRods.save_metadata")
    if (__SESSION__ is None):
        connect(options)
    print("iRods.save_metadata: SESSION={}".format(__SESSION__))

    # print(str(metadata))
    print("TESTING: {}".format(fits_file))
    test(fits_file, options)
