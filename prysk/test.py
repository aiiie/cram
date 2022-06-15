"""Utilities for running individual tests"""

import itertools
import os
import re
import time
from contextlib import contextmanager
from pathlib import Path

from prysk.diff import esc, glob, regex, unified_diff
from prysk.process import PIPE, STDOUT, execute

__all__ = ["test", "testfile", "runtests"]

_SKIP = 80
_IS_ESCAPING_NEEDED = re.compile(rb"[\x00-\x09\x0b-\x1f\x7f-\xff]").search


def _escape(s):
    """Like the string-escape codec, but doesn't escape quotes"""
    escape_sub = re.compile(rb"[\x00-\x09\x0b-\x1f\\\x7f-\xff]").sub
    escape_map = dict((bytes([i]), rb"\x%02x" % i) for i in range(256))
    escape_map.update({b"\\": b"\\\\", b"\r": rb"\r", b"\t": rb"\t"})
    return escape_sub(lambda m: escape_map[m.group(0)], s[:-1]) + b" (esc)\n"


def _findtests(paths):
    """Yield tests in paths in sorted order"""

    paths = list(map(Path, paths))

    def is_hidden(path):
        """Check if a path (file/dir) is hidden or not."""

        def _is_hidden(part):
            return (
                part.startswith(".")
                and not part == "."
                and not part.startswith("..")
                and not part.startswith("./")
            )

        return any(map(_is_hidden, path.parts))

    def is_testfile(path):
        """Check if path is a valid prysk test file"""
        return path.is_file() and path.suffix == ".t" and not is_hidden(path)

    def is_test_dir(path):
        """Check if the path is a valid prysk test dir"""
        return path.is_dir() and not is_hidden(path)

    def remove_duplicates(path):
        """Stable duplication removal"""
        return list(dict.fromkeys(path))

    def collect(paths):
        """Collect all test files compliant with cram collection order"""
        for path in paths:
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


def test(
    lines,
    shell="/bin/sh",
    indent=2,
    testname=None,
    env=None,
    cleanenv=True,
    debug=False,
):
    r"""Run test lines and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].

    Note that the TESTSHELL environment variable is available in the
    test (set to the specified shell). However, the TESTDIR and
    TESTFILE environment variables are not available. To run actual
    test files, see testfile().

    Example usage:

    >>> refout, postout, diff = test([b'  $ echo hi\n',
    ...                               b'  [a-z]{2} (re)\n'])
    >>> refout == [b'  $ echo hi\n', b'  [a-z]{2} (re)\n']
    True
    >>> postout == [b'  $ echo hi\n', b'  hi\n']
    True
    >>> bool(diff)
    False

    lines may also be a single bytes string:

    >>> refout, postout, diff = test(b'  $ echo hi\n  bye\n')
    >>> refout == [b'  $ echo hi\n', b'  bye\n']
    True
    >>> postout == [b'  $ echo hi\n', b'  hi\n']
    True
    >>> bool(diff)
    True
    >>> (b''.join(diff) ==
    ...  b'--- \n+++ \n@@ -1,2 +1,2 @@\n   $ echo hi\n-  bye\n+  hi\n')
    True

    :param lines: Test input
    :type lines: bytes or collections.Iterable[bytes]
    :param shell: Shell to run test in
    :type shell: bytes or str or list[bytes] or list[str]
    :param indent: Amount of indentation to use for shell commands
    :type indent: int
    :param testname: Optional test file name (used in diff output)
    :type testname: bytes or None
    :param env: Optional environment variables for the test shell
    :type env: dict or None
    :param cleanenv: Whether or not to sanitize the environment
    :type cleanenv: bool
    :param debug: Whether or not to run in debug mode (don't capture stdout)
    :type debug: bool
    return: Input, output, and diff iterables
    :rtype: (list[bytes], list[bytes], collections.Iterable[bytes])
    """
    indent = b" " * indent
    cmdline = indent + b"$ "
    conline = indent + b"> "
    salt = b"PRYSK%.5f" % time.time()

    def create_environment(environment, shell, clean=False):
        _env = os.environ.copy() if environment is None else environment
        _env["TESTSHELL"] = shell
        if clean:
            _env.update({key: "C" for key in ["LANG", "LC_ALL", "LANGUAGE"]})
            _env["TZ"] = "GMT"
            _env["CDPATH"] = ""
            _env["COLUMNS"] = "80"
            _env["GREP_OPTIONS"] = ""
        return _env

    lines = lines.splitlines(True) if isinstance(lines, bytes) else lines
    shell = [shell] if isinstance(shell, (bytes, str)) else shell
    env = create_environment(env, shell[0], clean=cleanenv)

    if debug:
        return _debug(cmdline, conline, env, lines, shell)

    after = {}
    refout, postout = [], []
    i = pos = prepos = -1
    stdin = []
    for i, line in enumerate(lines):
        if not line.endswith(b"\n"):
            line += b"\n"
        refout.append(line)
        if line.startswith(cmdline):
            after.setdefault(pos, []).append(line)
            prepos = pos
            pos = i
            stdin.append(b"echo %s %d $?\n" % (salt, i))
            stdin.append(line[len(cmdline) :])
        elif line.startswith(conline):
            after.setdefault(prepos, []).append(line)
            stdin.append(line[len(conline) :])
        elif not line.startswith(indent):
            after.setdefault(pos, []).append(line)
    stdin.append(b"echo %s %d $?\n" % (salt, i + 1))

    output, retcode = execute(
        shell + ["-"], stdin=b"".join(stdin), stdout=PIPE, stderr=STDOUT, env=env
    )
    if retcode == _SKIP:
        return refout, None, []

    pos = -1
    for i, line in enumerate(output[:-1].splitlines(True)):
        out, cmd = line, None
        if salt in line:
            out, cmd = line.split(salt, 1)

        if out:
            if not out.endswith(b"\n"):
                out += b" (no-eol)\n"

            if _IS_ESCAPING_NEEDED(out):
                out = _escape(out)
            postout.append(indent + out)

        if cmd:
            ret = int(cmd.split()[1])
            if ret != 0:
                postout.append(indent + b"[%d]\n" % ret)
            postout += after.pop(pos, [])
            pos = int(cmd.split()[0])

    postout += after.pop(pos, [])

    if testname:
        diff_path = bytes(testname)
        error_path = bytes(Path(testname.parent, f"{testname.name}.err"))
    else:
        diff_path = error_path = b""

    diff = unified_diff(
        refout, postout, diff_path, error_path, matchers=[esc, glob, regex]
    )
    for line in diff:
        return refout, postout, itertools.chain([line], diff)
    return refout, postout, []


def _debug(cmdline, conline, env, lines, shell):
    stdin = []
    for line in lines:
        if not line.endswith(b"\n"):
            line += b"\n"
        if line.startswith(cmdline):
            stdin.append(line[len(cmdline) :])
        elif line.startswith(conline):
            stdin.append(line[len(conline) :])
    execute(shell + ["-"], stdin=b"".join(stdin), env=env)
    return [], [], []


def testfile(
    path, shell="/bin/sh", indent=2, env=None, cleanenv=True, debug=False, testname=None
):
    """Run test at path and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].

    Note that the TESTDIR, TESTFILE, and TESTSHELL environment
    variables are available to use in the test.

    :param path: Path to test file
    :type path: bytes or str
    :param shell: Shell to run test in
    :type shell: bytes or str or list[bytes] or list[str]
    :param indent: Amount of indentation to use for shell commands
    :type indent: int
    :param env: Optional environment variables for the test shell
    :type env: dict or None
    :param cleanenv: Whether or not to sanitize the environment
    :type cleanenv: bool
    :param debug: Whether or not to run in debug mode (don't capture stdout)
    :type debug: bool
    :param testname: Optional test file name (used in diff output)
    :type testname: bytes or None
    :return: Input, output, and diff iterables
    :rtype: (list[bytes], list[bytes], collections.Iterable[bytes])
    """
    with open(path, "rb") as f:
        abspath = path.resolve()
        env = env or os.environ.copy()
        env["TESTDIR"] = f"{abspath.parent}"
        env["TESTFILE"] = f"{abspath.name}"
        if testname is None:
            testname = path
        return test(
            f,
            shell,
            indent=indent,
            testname=testname,
            env=env,
            cleanenv=cleanenv,
            debug=debug,
        )


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
