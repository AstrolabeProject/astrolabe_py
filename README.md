## Astrolabe Data Uploader

Author: Tom Hicks. 6/21/2018.

Purpose: Uploads FITS files to iRods, extracts and uploads metadata to iRods, creates and uploads WWT control files to iRods.

## Build

This software requires Python 3.6+. Within a virtual environment, do

```
   > pip install -r requirements.txt
   > pip install .
```

## Tests

```
   > cd test
   > python fits_meta_test.py
```

## Usage

To run the program:

```
   > 
```

Run Options:

```
Usage: astrolabe_uploader upload-directory-path
 -h,--help      Show usage information.
 -v,--verbose   Display more information.
```

Example Usage:

```
astrolabe_uploader -v myDataDirectory
```

## License

Licensed under Apache License Version 2.0.

(c) Astrolabe Project, The University of Arizona, 2018
