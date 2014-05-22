#!/usr/bin/env python
from distutils.core import setup

url = 'https://github.com/FEE1DE4D/KickassAPI'
setup(
    name='KickassAPI',
    version='1.0.0',
    py_modules=['KickassAPI'],

    author='FEE1DE4D',
    author_email='fee1de4d@gmail.com',

    url=url,
    description='Python API for kickass.to',
    license='GPLv2+',

    long_description="Documentation can be found here " + url,

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
