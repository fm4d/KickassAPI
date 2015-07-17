#!/usr/bin/env python
from distutils.core import setup

URL = 'https://github.com/FEE1DE4D/KickassAPI'
setup(
    name='KickassAPI',
    version='1.0.4',
    py_modules=['KickassAPI'],

    author='fm4d',
    author_email='m@fm4d.net',

    url=URL,
    description='Python API for kat.cr (formerly kickass.to)',
    license='GPLv2+',

    long_description="Documentation can be found here " + URL,

     install_requires=[
        'setuptools',
        'pyquery',
        'requests',
    ],

    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later ("
        "GPLv2+)",

        "Programming Language :: Python :: 2.7",

        "Development Status :: 3 - Alpha",

        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
