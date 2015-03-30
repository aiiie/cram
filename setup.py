#!/usr/bin/env python
"""Installs cram"""

import os
import pipes
import sys
from distutils.core import setup, Command, DistutilsError

COMMANDS = {}
CRAM_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    pass
else:
    COMMANDS['bdist_wheel'] = bdist_wheel

def _rundoctests():
    import cram
    import doctest
    import pkgutil

    if getattr(pkgutil, 'walk_packages', None) is not None:
        def getmodules():
            """Yield all cram modules"""
            yield cram
            path = cram.__path__
            for loader, name, ispkg in pkgutil.walk_packages(path):
                if name == '__main__':
                    continue
                yield loader.find_module(name).load_module(name)
    else:
        def getmodules():
            """Yield all cram modules"""
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
    return totalfailures

class doctest(Command):
    """Runs doctests"""
    description = 'run doctest test suite'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        failures = _rundoctests()
        if failures:
            raise DistutilsError('doctests failed')

COMMANDS['doctest'] = doctest

class test(Command):
    """Runs doctests and Cram tests"""
    description = 'run test suite'
    user_options = [('coverage', None, 'run tests using coverage.py'),
                    ('no-doctest', None, 'skip doctests'),
                    ('xunit-file=', None, 'path to write xUnit XML output')]

    def initialize_options(self):
        self.coverage = 0
        self.no_doctest = 0
        self.xunit_file = None

    def finalize_options(self):
        pass

    def run(self):
        import cram

        os.environ['PYTHON'] = sys.executable
        if self.coverage:
            # Note that when coverage.py is run, it uses the version
            # of Python it was installed with, NOT the version
            # setup.py was run with.
            os.environ['COVERAGE'] = '1'
            os.environ['COVERAGE_FILE'] = os.path.join(CRAM_DIR, '.coverage')

        args = ['-v']
        if self.xunit_file is not None:
            xunit_file = os.path.abspath(self.xunit_file)
            args.append('--xunit-file=%s' % pipes.quote(xunit_file))

        if not self.no_doctest:
            failures = _rundoctests()
        else:
            failures = 0

        ret = cram.main(args + ['tests'])
        if ret or failures:
            raise DistutilsError('tests failed')

COMMANDS['test'] = test

def long_description():
    """Get the long description from the README"""
    return open(os.path.join(sys.path[0], 'README.rst')).read()

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
    cmdclass=COMMANDS,
    description='A simple testing framework for command line applications',
    download_url='https://bitheap.org/cram/cram-0.6.tar.gz',
    keywords='automatic functional test framework',
    license='GNU GPL',
    long_description=long_description(),
    name='cram',
    packages=['cram'],
    scripts=['scripts/cram'],
    url='https://bitheap.org/cram/',
    version='0.6',
)
