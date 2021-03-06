#!/usr/bin/env python

# Copyright 2014 John C. Earls
#
#This file is part of AUREA Nebula 
#
#AUREA Nebula is free software:
#AUREA Nebula  is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


#Note: credit where credit is due.  This setup.py is based on 
#Starcluster's https://github.com/jtriley/StarCluster

import os
import sys

if sys.version_info < (2, 7):
    error = "ERROR: ansnapr  requires Python 2.7+ ... exiting."
    print >> sys.stderr, error
    sys.exit(1)

from setuptools import setup, find_packages
console_scripts = [ 'ansnapr = ansnapr.server:main',
        'ansnapr-logserver = ansnapr.utils.debug:startLogger' ]
extra = dict(install_requires=["boto>=2.9.9","mpi4py>=1.2.2" ],
            entry_points=dict(console_scripts=console_scripts), 
             zip_safe=False)
VERSION = '0.0.0'#actually set in utils.static
static = os.path.join('ansnapr','utils','static.py')
execfile(static)

setup(
name='AN-snapr',
version=VERSION,
packages=find_packages(),
license='AGPL',
author='John C. Earls',
author_email='john.c.earls@gmail.com',
url="https://github.com/JohnCEarls/AN-snapr",
description="A server to interface with snapr in AUREA Nebula",
classifiers=[
    'Environment :: Console',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Library or Lesser General Public '
    'License (AGPL)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Operating System :: Linux',
    'Operating System :: POSIX',
    'Topic :: Education',
    'Topic :: Scientific/Engineering',
    'Topic :: System :: Distributed Computing',
    'Topic :: Software Development :: Libraries :: Python Modules',
],
**extra
)
