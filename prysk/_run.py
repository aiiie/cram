"""The test runner"""

import os
import sys
from contextlib import contextmanager

from prysk._test import testfile

__all__ = ["runtests"]

if sys.platform == "win32":

    def _walk(top):
        top = os.fsdecode(top)
        for root, dirs, files in os.walk(top):
            yield (
                os.fsencode(root),
                [os.fsencode(p) for p in dirs],
                [os.fsencode(p) for p in files],
            )

else:
    _walk = os.walk


def _findtests(paths):
    """Yield tests in paths in sorted order"""
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in _walk(p):
                if os.path.basename(root).startswith(b"."):
                    continue
                for f in sorted(files):
                    if not f.startswith(b".") and f.endswith(b".t"):
                        yield os.path.normpath(os.path.join(root, f))
        else:
            yield os.path.normpath(p)


@contextmanager
def _cwd(path):
    """Change the working directory

    This context manager will change the working directory
    and restore it afterwards.
    """
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(cwd)


def runtests(paths, tmpdir, shell, indent=2, cleanenv=True, debug=False):
    """Run tests and yield results.

    This yields a sequence of 2-tuples containing the following:

        (test path, test function)

    The test function, when called, runs the test in a temporary directory
    and returns a 3-tuple:

        (list of lines in the test, same list with actual output, diff)
    """
    seen = set()
    basenames = set()
    for i, path in enumerate(_findtests(paths)):
        abspath = os.path.abspath(path)
        if abspath in seen:
            continue
        seen.add(abspath)

        if not os.stat(path).st_size:
            yield (path, lambda: (None, None, None))
            continue

        basename = os.path.basename(path)
        if basename in basenames:
            basename = basename + b"-%d" % i
        else:
            basenames.add(basename)

        def test():
            """Run test file"""
            testdir = os.path.join(tmpdir, basename)
            os.mkdir(testdir)
            with _cwd(testdir):
                return testfile(
                    abspath,
                    shell,
                    indent=indent,
                    cleanenv=cleanenv,
                    debug=debug,
                    testname=path,
                )

        yield (path, test)
