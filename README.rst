Astrolabe Python Library
========================

:Version: 0.0.12
:Author: Tom Hicks <hickst@email.arizona.edu>

| This is a Python 3 library for curating image and data files for the `Astrolabe project <http://astrolabe.arizona.edu/>`_

- Astrolabe_py contains scripts and modules to:

  - Upload FITS files to iRods,
  - Extract metadata from FITS files and attach it to files in iRods,


Building from Source
--------------------

Use of this software requires `Python 3.6+`. Within a virtual environment, do::

   pip install -r requirements.txt
   pip install .


Running Tests
-------------

The tests can be run manually from the `test` subdirectory, as follows::

  cd test
  python fits_ops_test.py
  python fits_meta_test.py
  python irods_help_test.py
  python uploader.py


Run the Scripts
---------------

To run a script::

   python uploader


Uploader Script Options::


  usage: uploader [-h] [-v] [-u] [--version] [--keyfile [metadata-keyfile]] images_path

  FITS file metadata extraction and upload of a file or directory of files.

  positional arguments:
     images_path           path to a FITS file or a directory of FITS files to be processed

  optional arguments:
     -h, --help            show this help message and exit
     -v, --verbose         provide more information during execution
     -u, --upload-only     upload files to iRods only: do not process file metadata
     --version             show program's version number and exit
     --keyfile [metadata-keyfile]
                           a file specifying which metadata keys which should be processed


Examples::

  uploader -v myDataDirectory
  uploader --upload-only myImages/someImage.fits
  uploader --keyfile just-these-keys.txt astrofiles


Documentation
-------------

The User and API documentation is written in ReStructuredText, and can
be built using `sphinx <http://www.sphinx-doc.org/>`_::

    python setup.py userdoc
    python setup.py apidoc

The documentation will be generated and saved in ``userdoc/html/`` and
``apidoc/html/``.


License
-------

Licensed under Apache License Version 2.0.

Copyright 2018 by Astrolabe Project: American Astronomical Society and the University of Arizona.
