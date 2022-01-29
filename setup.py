#!/usr/bin/env python
"""Installs prysk"""
import os
import sys
from distutils.core import setup

COMMANDS = {}
try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    pass
else:
    COMMANDS['bdist_wheel'] = bdist_wheel


def readme():
    with open(os.path.join(sys.path[0], 'README.rst')) as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='prysk',
        author='Brodie Rao, Nicola Coretti',
        author_email='brodie@bitheap.org, nico.coretti@gmail.com',
        version='0.9',
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
        keywords='automatic functional test framework, snapshot testing',
        url='https://github.com/Nicoretti/prysk',
        license='GNU GPLv2 or any later version',
        long_description=readme(),
        entry_points={
            'console_scripts': [
                'prysk=prysk:cli.main',
            ],
        },
    )
