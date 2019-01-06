#!/usr/bin/env python
#
# Setup script.
#   Written by: Tom Hicks. 6/22/2018.
#   Last Modified: Figure out requires. Redo VERSION reading.
#
import os
import re
import sys
from setuptools import setup, find_packages

# Eval the VERSION number from the version file
with open('astrolabe_py/version.py') as vfile:
    exec(vfile.read())

# Read in the long description from the README file
with open("README.rst", "r", encoding="UTF-8") as rm:
    long_description = rm.read()

# Build the list of scripts to be installed.
# script_dir = 'scripts'
# scripts = []
# for script in os.listdir(script_dir):
#     scripts.append(os.path.join(script_dir,script))

setup(
    name="astrolabe_py",
    version=VERSION,
    author="Tom Hicks",
    author_email="hickst@email.arizona.edu",
    description="Tools for working with Astrolabe data.",
    license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/AstrolabeProject/astrolabe_py",
    packages=find_packages(exclude=['test.*']),
    package_data ={
        'astrolabe_py': ['data/*']
    },
    install_requires=[
        'astropy>=3.0.3',
        'python-irodsclient>=0.8.1'
    ],
    python_requires='~=3.6',
    # scripts=scripts,
    scripts=[ "checker", "uploader" ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving',
    ],
    keywords='Astrolabe datastore iRods metadata uploading'
)
