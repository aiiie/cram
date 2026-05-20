"""Utilities for running individual tests"""

import itertools
import os
import re
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import NamedTuple

from cram._diff import esc, glob, regex, unified_diff
from cram._process import ErrMode, OutMode, execute

__all__ = ['Test', 'TestResult', 'test', 'testfile']

_needescape = re.compile(br'[\x00-\x09\x0b-\x1f\x7f-\xff]').search
_escapesub = re.compile(br'[\x00-\x09\x0b-\x1f\\\x7f-\xff]').sub
_escapemap = {bytes([i]): br'\x%02x' % i for i in range(256)}
_escapemap |= {b'\\': b'\\\\', b'\r': br'\r', b'\t': br'\t'}

def _escape(s: bytes) -> bytes:
    """Like the string-escape codec, but doesn't escape quotes"""
    return (_escapesub(lambda m: _escapemap[m.group(0)], s[:-1]) +
            b' (esc)\n')

def _decodeargs(args: Sequence[bytes | str]) -> list[str]:
    """Normalize path arguments to strs"""
    return [os.fsdecode(a) for a in args]

def _decodeenv(env: (Mapping[bytes, bytes | str] | Mapping[str, bytes | str] |
                     Mapping[bytes | str, bytes | str])) -> dict[str, str]:
    """Normalize environment variables to strs"""
    return {os.fsdecode(k): os.fsdecode(v) for k, v in env.items()}

class TestResult(NamedTuple):
    """The result of running a test.

    This contains the original reference output (in other words, lines in the
    test), the same lines but with the expected output lines replaced with the
    actual output, and unified diff between the two (with special matching
    syntax such as (esc), (glob), (re), etc. handled appropriately).
    """

    refout: list[bytes] | None
    postout: list[bytes] | None
    diff: Iterable[bytes] | None

class Test(NamedTuple):
    """Test file and associated test function.

    This is used by test runners (e.g., runtests(), runcli(), runxunit()) to
    yield a list of tests and functions to run them. Runners can wrap the
    resulting run functions to support composition.
    """

    path: str
    run: Callable[[], TestResult]

def test(lines: bytes | Iterable[bytes],
         shell: bytes | str | Sequence[bytes | str]='/bin/sh', indent: int=2,
         testname: bytes | str | None=None,
         env: (Mapping[bytes, bytes | str] | Mapping[str, bytes | str] |
               Mapping[bytes | str, bytes | str] | None)=None,
         cleanenv: bool=True, debug: bool=False) -> TestResult:
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
    :type testname: bytes or str or None
    :param env: Optional environment variables for the test shell
    :type env: dict[bytes, bytes] or dict[str, str] or None
    :param cleanenv: Whether or not to sanitize the environment
    :type cleanenv: bool
    :param debug: Whether or not to run in debug mode (don't capture stdout)
    :type debug: bool
    return: Input, output, and diff iterables
    :rtype: TestResult
    """
    indentws = b' ' * indent
    cmdline = indentws + b'$ '
    conline = indentws + b'> '
    salt = b'CRAM%.5f' % time.time()

    env = _decodeenv(env) if env is not None else os.environ.copy()
    if cleanenv:
        for s in ('LANG', 'LC_ALL', 'LANGUAGE'):
            env[s] = 'C'
        env['TZ'] = 'GMT'
        env['CDPATH'] = ''
        env['COLUMNS'] = '80'
        env['GREP_OPTIONS'] = ''

    if isinstance(lines, bytes):
        lines = lines.splitlines(True)

    shell = _decodeargs([shell] if isinstance(shell, (bytes, str)) else shell)
    env['TESTSHELL'] = os.fsdecode(shell[0])

    stdin: list[bytes] = []

    if debug:
        for line in lines:
            if not line.endswith(b'\n'):
                line += b'\n'
            if line.startswith(cmdline):
                stdin.append(line[len(cmdline):])
            elif line.startswith(conline):
                stdin.append(line[len(conline):])

        execute([*shell, '-'], stdin=b''.join(stdin), env=env)
        return TestResult([], [], None)

    after: dict[int, list[bytes]] = {}
    refout: list[bytes] = []
    postout: list[bytes] = []
    i = pos = prepos = -1
    for i, line in enumerate(lines):
        if not line.endswith(b'\n'):
            line += b'\n'
        refout.append(line)
        if line.startswith(cmdline):
            after.setdefault(pos, []).append(line)
            prepos = pos
            pos = i
            stdin.extend([b'echo %s %d $?\n' % (salt, i),
                          line[len(cmdline):]])
        elif line.startswith(conline):
            after.setdefault(prepos, []).append(line)
            stdin.append(line[len(conline):])
        elif not line.startswith(indentws):
            after.setdefault(pos, []).append(line)
    stdin.append(b'echo %s %d $?\n' % (salt, i + 1))

    output, retcode = execute([*shell, '-'], stdin=b''.join(stdin),
                              stdout=OutMode.PIPE, stderr=ErrMode.STDOUT,
                              env=env)
    if retcode == 80:
        return TestResult(refout, None, None)

    pos = -1
    ret = 0
    for line in output[:-1].splitlines(True):
        out, cmd = line, None
        if salt in line:
            out, cmd = line.split(salt, 1)

        if out:
            if not out.endswith(b'\n'):
                out += b' (no-eol)\n'

            if _needescape(out):
                out = _escape(out)
            postout.append(indentws + out)

        if cmd:
            ret = int(cmd.split()[1])
            if ret != 0:
                postout.append(indentws + b'[%d]\n' % ret)
            postout += after.pop(pos, [])
            pos = int(cmd.split()[0])

    postout += after.pop(pos, [])

    if testname:
        diffpath = os.fsencode(testname)
        errpath = diffpath + b'.err'
    else:
        diffpath = errpath = b''
    diffgen = unified_diff(refout, postout, diffpath, errpath,
                           matchers=[esc, glob, regex])
    firstline = next(diffgen, None)
    diff = (itertools.chain([firstline], diffgen)
            if firstline is not None else None)
    return TestResult(refout, postout, diff)

def testfile(path: bytes | str,
             shell: bytes | str | Sequence[bytes | str]=b'/bin/sh',
             indent: int=2,
             env: (Mapping[bytes, bytes | str] | Mapping[str, bytes | str] |
                   Mapping[bytes | str, bytes | str] | None)=None,
             cleanenv: bool=True,
             debug: bool=False, testname: bytes | str | None=None
             ) -> TestResult:
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
    :type env: dict[bytes, bytes] or dict[str, str] or None
    :param cleanenv: Whether or not to sanitize the environment
    :type cleanenv: bool
    :param debug: Whether or not to run in debug mode (don't capture stdout)
    :type debug: bool
    :param testname: Optional test file name (used in diff output)
    :type testname: bytes or str or None
    :return: Input, output, and diff iterables
    :rtype: TestResult
    """
    path = os.fsdecode(path)
    abspath = os.path.abspath(path)
    testdir = os.path.dirname(abspath)
    testfile = os.path.basename(abspath)
    env = _decodeenv(env) if env is not None else os.environ.copy()
    env['TESTDIR'] = testdir
    env['TESTFILE'] = testfile
    if testname is None: # pragma: nocover
        testname = os.path.basename(abspath)

    with open(path, 'rb') as f:
        return test(f, shell, indent=indent, testname=testname, env=env,
                    cleanenv=cleanenv, debug=debug)
