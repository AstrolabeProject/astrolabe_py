## Astrolabe Data Uploader

Author: Tom Hicks. 6/21/2018.

Purpose: Uploads FITS files to iRods, extracts and uploads metadata to iRods, creates and uploads WWT control files to iRods.

## Build

This software requires Python 3.6+.

```
   > gradle clean build
```

## Usage

To run the JAR file:

```
   > java -jar applicantToCsv.jar input-JSON-file
```

Run Options:

```
Usage: java -jar applicantToCsv.jar [-h] [-v] input-JSON-file
 -h,--help      Show usage information.
 -v,--verbose   Display more information.
```

Example Usage:

```
java -jar applicantToCsv.jar applicants-2017.json
```

## License

Licensed under Apache License Version 2.0.

(c) Astrolabe Project, The University of Arizona, 2018
