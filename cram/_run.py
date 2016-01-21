"""The test runner"""

import os

from cram._encoding import b
from cram._test import testfile

__all__ = ['runtests']

def _findtests(paths):
    """Yield tests in paths in sorted order"""
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                if os.path.basename(root).startswith(b('.')):
                    continue
                for f in sorted(files):
                    if not f.startswith(b('.')) and f.endswith(b('.t')):
                        yield os.path.normpath(os.path.join(root, f))
        else:
            yield os.path.normpath(p)

def runtests(paths, tmpdir, shell, indent=2, cleanenv=True, debug=False):
    """Run tests and yield results.

    This yields a sequence of 3-tuples containing the following:

        (test path, absolute test path, test function)

    The test function, when called, runs the test in a temporary directory
    and returns a 3-tuple:

        (list of lines in the test, same list with actual output, diff)
    """
    cwd = os.getcwd()
    seen = set()
    basenames = set()
    for i, path in enumerate(_findtests(paths)):
        abspath = os.path.abspath(path)
        if abspath in seen:
            continue
        seen.add(abspath)

        if not os.stat(abspath).st_size:
            yield (path, abspath, lambda: (None, None, None))
            continue

        basename = os.path.basename(path)
        if basename in basenames:
            basename = basename + b('-%s' % i)
        else:
            basenames.add(basename)

        def test():
            """Run test file"""
            testdir = os.path.join(tmpdir, basename)
            os.mkdir(testdir)
            try:
                os.chdir(testdir)
                return testfile(abspath, shell, indent=indent,
                                cleanenv=cleanenv, debug=debug)
            finally:
                os.chdir(cwd)

        yield (path, abspath, test)
