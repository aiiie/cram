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
        import difflib
        import doctest
        import cram
        failures, tests = doctest.testmod(cram)
        print 'doctests: %s/%s passed' % (tests - failures, tests)
        print 'cram:',
        a = ['tests/bare.t: passed\n',
             'tests/empty.t: empty\n',
             'tests/fail.t: failed\n',
             '--- tests/fail.t \n',
             '+++ tests/fail.t.out \n',
             '@@ -3,6 +3,6 @@\n',
             '   $ echo 1\n',
             '   1\n',
             '   $ echo 1\n',
             '-  2\n',
             '+  1\n',
             '   $ echo 1\n',
             '   1\n',
             'tests/test.t: passed\n']
        b = ''.join(cram.run(['.'], verbose=True)).splitlines(True)
        diff = ''.join(difflib.unified_diff(a, b))
        if diff:
            print
            print diff
        else:
            print 'passed'

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
