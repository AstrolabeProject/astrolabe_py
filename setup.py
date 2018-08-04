import os
import re
import sys
from setuptools import setup, find_packages

# Get the version number from the package itself
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('astrolabe_uploader/__init__.py').read(),
    re.M
).group(1)


# Read in the long description from the README file
with open("README.rst", "r", encoding="UTF-8") as rm:
    long_description = rm.read()

# Build the list of scripts to be installed.
# script_dir = 'scripts'
# scripts = []
# for script in os.listdir(script_dir):
#     scripts.append(os.path.join(script_dir,script))

setup(
    name="astrolabe_uploader",
    version=version,
    author="Tom Hicks",
    author_email="hickst@email.arizona..edu",
    description="Tools for working with Astrolabe data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AstrolabeProject/astrolabe_uploader",
    packages=find_packages(exclude=['test.*']),
    package_data ={
        'astrolabe_uploader': ['data/*']
    },
    # scripts=scripts,
    scripts=[ "checker", "uploader" ]
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License :: 2',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving',
    ],
    keywords='Astrolabe datastore iRods metadata uploading'
)
