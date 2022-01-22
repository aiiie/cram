#!/usr/bin/env python
"""Installs prysk"""
import os
import sys
from distutils.core import setup

COMMANDS = {}
CRAM_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    pass
else:
    COMMANDS['bdist_wheel'] = bdist_wheel

def long_description():
    """Get the long description from the README"""
    return open(os.path.join(sys.path[0], 'README.rst')).read()

# TODO:
# Add:
#  * url
#  * download_url
#  * keyword (snapshot test tool)
setup(
    name='prysk',
    author='Brodie Rao, Nicola Coretti',
    author_email='brodie@bitheap.org, nico.coretti@gmail.com',
    version='0.8',
    packages=['prysk'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ('License :: OSI Approved :: GNU General Public License v2 '
         'or later (GPLv2+)'),
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Testing',
    ],
    cmdclass=COMMANDS,
    description='Functional tests for command line applications',
    keywords='automatic functional test framework',
    license='GNU GPLv2 or any later version',
    long_description=long_description(),
    entry_points={
        'console_scripts': [
            'prysk=prysk:cli.main',
        ],
    },
)
