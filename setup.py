from setuptools import setup, find_packages
import os
import sys

with open("README.md", "r", encoding="UTF-8") as rm:
    long_description = rm.read()

## Build the list of scripts to be installed.
script_dir = 'scripts'
scripts = []
for script in os.listdir(script_dir):
    if script[-1] in [ "~", "#"]:
        continue
    scripts.append(os.path.join(script_dir,script))

setup(
    name="astrolabe_uploader",
    version="0.0.1",
    author="Tom Hicks",
    author_email="hickst@email.arizona..edu",
    description="Tools for uploading Astrolabe data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AstrolabeProject/astrolabe_uploader",
    packages=find_packages(exclude=['test.*']),
    package_data ={
        'astrolabe_uploader': ['data/*']
    },
    scripts=scripts,
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
    keywords='datastore iRods metadata uploading WWT'
)
