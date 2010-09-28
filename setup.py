#!/usr/bin/env python

import os
import sys
from distutils.core import setup, Command

class test(Command):
    description = 'run test suite'
    user_options = [('coverage', None, 'run tests using coverage.py')]

    def initialize_options(self):
        self.coverage = 0

    def finalize_options(self):
        pass

    def run(self):
        import doctest
        import cram
        failures, tests = doctest.testmod(cram)
        sys.stdout.write('doctests: %s/%s passed\n' %
                         (tests - failures, tests))
        os.environ['PYTHON'] = sys.executable
        if self.coverage:
            # Note that when coverage.py is run, it uses the version
            # of Python it was installed with, NOT the version
            # setup.py was run with.
            os.environ['COVERAGE'] = '1'
            os.environ['COVERAGE_FILE'] = os.path.abspath('./.coverage')
        cram.main(['-v', 'tests'])

def long_description():
    try:
        return open(os.path.join(sys.path[0], 'README.txt')).read()
    except Exception:
        return """
Cram is a functional testing framework for command line applications
based on Mercurial_'s `unified test format`_.

.. _Mercurial: http://mercurial.selenic.com/
.. _unified test format: http://www.selenic.com/blog/?p=663
"""

setup(
    author='Brodie Rao',
    author_email='brodie@bitheap.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Testing',
    ],
    cmdclass={'test': test},
    description='A simple testing framework for command line applications',
    download_url='http://bitheap.org/cram/cram-0.4.tar.gz',
    keywords='automatic functional test framework',
    license='GNU GPL',
    long_description=long_description(),
    name='cram',
    py_modules=['cram'],
    scripts=['scripts/cram'],
    url='http://bitheap.org/cram/',
    version='0.4',
)
