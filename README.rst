Astrolabe Python Library
========================

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

:Version: 1.0.1
:Author: Tom Hicks <hickst@email.arizona.edu>

| This is a Python 3 library for curating image and data files for the `Astrolabe project <http://astrolabe.arizona.edu/>`_

- Astrolabe_py contains scripts and modules to:

  - Check FITS file metadata for validity,
  - Show FITS file HDU information,
  - Upload FITS files to iRods, optionally extracting FITS metadata and attaching
    it to the uploaded files in iRods.


Installation
------------

Install via `PyPi <https://pypi.org/project/astrolabe-py/>`_

   pip install astrolabe-py


Python Build using Conda
------------------------

Building this software requires ``Python 3.6+``. Assuming you have ``Conda`` installed,
you can use it to build this project within a virtual environment::

   git clone https://github.com/AstrolabeProject/astrolabe_py.git
   source activate
   conda create -n alpy python=3.6
   conda activate alpy
   cd astrolabe_py
   pip install -r requirements.txt


Running Tests
-------------

The tests can be run manually from the ``test`` subdirectory, as follows::

  cd test
  python fits_ops_test.py
  python fits_meta_test.py
  python irods_help_test.py
  python uploader_test.py


Running the Uploader Script
---------------------------

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


Running the Checker Script
--------------------------

Checker Script Options::

  usage: checker [-h] [-a {check,info}] [-v] [--version] images_path

  Perform verification actions on a FITS file or a directory of FITS files OR
  Show HDU info for the specified FITS file or directory of FITS files

  positional arguments:
    images_path           path to a FITS file or a directory of FITS files to be processed

  optional arguments:
    -h, --help            show this help message and exit
    -a {check,info}, --action {check,info}
                          action to perform on FITS file(s): validate or show HDU info
    --version             show program's version number and exit

Examples::

  checker myDataDirectory
  checker -a check myDataDirectory

  checker myImages/someImage.fits
  checker -a check myImages/someImage.fits

  checker -a info myDataDirectory
  checker -a info myImages/someImage.fits


License
-------

Licensed under Apache License Version 2.0.

Copyright 2018 by Astrolabe Project: American Astronomical Society and the University of Arizona.
