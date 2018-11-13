Astrolabe Python Library
========================

:Version: 0.0.20
:Author: Tom Hicks <hickst@email.arizona.edu>

| This is a Python 3 library for curating image and data files for the `Astrolabe project <http://astrolabe.arizona.edu/>`_

- Astrolabe_py contains scripts and modules to:

  - Upload FITS files to iRods,
  - Extract metadata from FITS files and attach it to files in iRods,


Python Build using Conda
------------------------

Building this software requires `Python 3.6+`. Assuming you have `Conda` installed,
you can use it to build this project within a virtual environment::

   git clone https://github.com/AstrolabeProject/astrolabe_py.git
   source activate
   conda create -n alpy python=3.6
   conda activate alpy
   cd astrolabe_py
   pip install -r requirements.txt


Running Tests
-------------

The tests can be run manually from the `test` subdirectory, as follows::

  cd test
  python fits_ops_test.py
  python fits_meta_test.py
  python irods_help_test.py
  python uploader_test.py


Build a Docker Image
--------------------

:TODO: Add this documentation.


Run the Uploader Script
-----------------------

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
be built using `sphinx <http://www.sphinx-doc.org/>`_.


License
-------

Licensed under Apache License Version 2.0.

Copyright 2018 by Astrolabe Project: American Astronomical Society and the University of Arizona.
