#!/usr/bin/env python

from distutils.core import setup, Command

class test(Command):
    description = 'run test suite'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import doctest
        import os
        import sys
        import cram
        failures, tests = doctest.testmod(cram)
        sys.stdout.write('doctests: %s/%s passed\n' % (tests - failures, tests))
        os.environ['PYTHON'] = sys.executable
        cram.main(['-v', 'tests'])

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
    description='',
    download_url='http://bitheap.org/cram/cram-0.1.tar.gz',
    keywords='automatic functional test framework',
    license='GNU GPL',
    long_description="""
Cram is a testing framework for command line applications based on
Mercurial_'s `unified test format`_.

.. _Mercurial: http://mercurial.selenic.com/
.. _unified test format: http://www.selenic.com/blog/?p=663
""",
    name='cram',
    py_modules=['cram'],
    scripts=['scripts/cram'],
    url='http://bitheap.org/cram/',
    version='0.1',
)
