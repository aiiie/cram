"""The test runner"""

import os
from contextlib import contextmanager
from pathlib import Path

from prysk.test import testfile

__all__ = ["runtests"]


def _findtests(paths):
    """Yield tests in paths in sorted order"""

    paths = list(map(Path, paths))

    def is_hidden(p):
        """Check if a path (file/dir) is hidden or not."""
        return any(map(lambda part: part.startswith("."), p.parts))

    def is_testfile(p):
        """Check if path is a valid prysk test file"""
        return p.is_file() and p.suffix == ".t" and not is_hidden(p)

    def is_test_dir(p):
        """Check if the path is a valid prysk test dir"""
        return p.is_dir() and not is_hidden(p)

    def remove_duplicates(p):
        """Stable duplication removal"""
        return list(dict.fromkeys(p))

    def collect(p):
        """Collect all test files compliant with cram collection order"""
        for path in p:
            if is_testfile(path):
                yield path
            if is_test_dir(path):
                yield from sorted((f for f in path.rglob("*.t") if is_testfile(f)))

    yield from remove_duplicates(collect(paths))


@contextmanager
def cwd(path):
    """Change the current working directory and restore it afterwards."""
    _cwd = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(_cwd)


def runtests(paths, tmpdir, shell, indent=2, cleanenv=True, debug=False):
    """Run tests and yield results.

    This yields a sequence of 2-tuples containing the following:

        (test path, test function)

    The test function, when called, runs the test in a temporary directory
    and returns a 3-tuple:

        (list of lines in the test, same list with actual output, diff)
    """
    basenames, seen = set(), set()
    tests = _findtests(paths)
    for i, path in enumerate(tests):
        abspath = path.resolve()
        if abspath in seen:
            continue
        seen.add(abspath)

        if not path.stat().st_size:
            yield path, lambda: (None, None, None)
            continue

        basename = path.name
        if basename in basenames:
            basename = f"{basename}-{i}"
        else:
            basenames.add(basename)

        def test():
            """Run test file"""
            testdir = tmpdir / basename
            os.mkdir(testdir)
            with cwd(testdir):
                return testfile(
                    abspath,
                    shell,
                    indent=indent,
                    cleanenv=cleanenv,
                    debug=debug,
                    testname=path,
                )

        yield path, test
