"""The test runner"""

import os
from collections.abc import Iterable

from cram._test import testfile, Test, TestResult

__all__ = ['runtests']

def _findtests(paths: list[str]) -> Iterable[str]:
    """Yield tests in paths in sorted order"""
    for p in paths:
        if os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                if os.path.basename(root).startswith('.'):
                    continue
                for f in sorted(files):
                    if not f.startswith('.') and f.endswith('.t'):
                        yield os.path.normpath(os.path.join(root, f))
        else:
            yield os.path.normpath(p)

def runtests(paths: list[str], tmpdir: str, shell: list[str],
             indent: int=2, cleanenv: bool=True, debug: bool=False
             ) -> Iterable[Test]:
    """Run tests and yield results.

    This yields a sequence of 2-tuples containing the following:

        (test path, test function)

    The test function, when called, runs the test in a temporary directory
    and returns a 3-tuple:

        (list of lines in the test, same list with actual output, diff)
    """
    cwd = os.getcwd()
    seen: set[str] = set()
    basenames: set[str] = set()
    for i, path in enumerate(_findtests(paths)):
        abspath = os.path.abspath(path)
        if abspath in seen:
            continue
        seen.add(abspath)

        if not os.stat(path).st_size:
            yield Test(path, lambda: TestResult(None, None, None))
            continue

        basename = os.path.basename(path)
        if basename in basenames:
            basename = f'{basename}-{i}'
        else:
            basenames.add(basename)

        def test() -> TestResult:
            """Run test file"""
            testdir = os.path.join(tmpdir, basename)
            os.mkdir(testdir)
            try:
                os.chdir(testdir)
                return testfile(abspath, shell, indent=indent,
                                cleanenv=cleanenv, debug=debug,
                                testname=path)
            finally:
                os.chdir(cwd)

        yield Test(path, test)
