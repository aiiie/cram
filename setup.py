#!/usr/bin/env python
"""Installs cram"""

import os
import sys
from distutils.core import setup, Command

CRAM_DIR = os.path.dirname(__file__)

class test(Command):
    """Runs doctests and Cram tests"""
    description = 'run test suite'
    user_options = [('coverage', None, 'run tests using coverage.py')]

    def initialize_options(self):
        self.coverage = 0

    def finalize_options(self):
        pass

    def run(self):
        import doctest
        import cram
        import pkgutil

        if getattr(pkgutil, 'walk_packages', None) is not None:
            def getmodules():
                yield cram
                for loader, name, ispkg in pkgutil.walk_packages(cram.__path__):
                    if name == '__main__':
                        continue
                    yield loader.find_module(name).load_module(name)
        else:
            def getmodules():
                pkgdir = os.path.join(CRAM_DIR, 'cram')
                for root, dirs, files in os.walk(pkgdir):
                    if '__pycache__' in dirs:
                        dirs.remove('__pycache__')
                    for fn in files:
                        if not fn.endswith('.py') or fn == '__main__.py':
                            continue

                        modname = fn.replace(os.sep, '.')[:-len('.py')]
                        if modname.endswith('.__init__'):
                            modname = modname[:-len('.__init__')]
                        modname = '.'.join(['cram', modname])
                        if '.' in modname:
                            fromlist = [modname.rsplit('.', 1)[1]]
                        else:
                            fromlist = []

                        yield __import__(modname, {}, {}, fromlist)

        totalfailures = totaltests = 0
        for module in getmodules():
            failures, tests = doctest.testmod(module)
            totalfailures += failures
            totaltests += tests
        sys.stdout.write('doctests: %s/%s passed\n' %
                         (totaltests - totalfailures, totaltests))

        os.environ['PYTHON'] = sys.executable
        if self.coverage:
            # Note that when coverage.py is run, it uses the version
            # of Python it was installed with, NOT the version
            # setup.py was run with.
            os.environ['COVERAGE'] = '1'
            os.environ['COVERAGE_FILE'] = os.path.join(CRAM_DIR, '.coverage')
        cram.main(['-v', 'tests'])

def long_description():
    """Get the long description from the README"""
    return open(os.path.join(sys.path[0], 'README.txt')).read()

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
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Testing',
    ],
    cmdclass={'test': test},
    description='A simple testing framework for command line applications',
    download_url='https://bitheap.org/cram/cram-0.6.tar.gz',
    keywords='automatic functional test framework',
    license='GNU GPL',
    long_description=long_description(),
    name='cram',
    py_modules=['cram'],
    scripts=['scripts/cram'],
    url='https://bitheap.org/cram/',
    version='0.6',
)
