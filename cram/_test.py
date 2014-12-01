"""Utilities for running individual tests"""

import itertools
import os
import re
import time

from cram._encoding import b, bchr, fsdecode
from cram._diff import glob, regex, unified_diff
from cram._process import PIPE, STDOUT, execute

__all__ = ['test', 'testfile']

_needescape = re.compile(b(r'[\x00-\x09\x0b-\x1f\x7f-\xff]')).search
_escapesub = re.compile(b(r'[\x00-\x09\x0b-\x1f\\\x7f-\xff]')).sub
_escapemap = dict((bchr(i), b(r'\x%02x' % i)) for i in range(256))
_escapemap.update({b('\\'): b('\\\\'), b('\r'): b(r'\r'), b('\t'): b(r'\t')})

def _escape(s):
    """Like the string-escape codec, but doesn't escape quotes"""
    return (_escapesub(lambda m: _escapemap[m.group(0)], s[:-1]) +
            b(' (esc)\n'))

def test(lines, shell, indent=2, testname=None, env=None, cleanenv=True):
    """Run test lines and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].

    Note that the TESTDIR and TESTFILE environment variables are not
    available when running tests with this function. To run actual
    test files, see testfile().
    """
    indent = b(' ') * indent
    cmdline = indent + b('$ ')
    conline = indent + b('> ')
    usalt = 'CRAM%s' % time.time()
    salt = b(usalt)

    env = env or os.environ.copy()
    if cleanenv:
        for s in ('LANG', 'LC_ALL', 'LANGUAGE'):
            env[s] = 'C'
        env['TZ'] = 'GMT'
        env['CDPATH'] = ''
        env['COLUMNS'] = '80'
        env['GREP_OPTIONS'] = ''

    after = {}
    refout, postout = [], []
    i = pos = prepos = -1
    stdin = []
    for i, line in enumerate(lines):
        refout.append(line)
        if line.startswith(cmdline):
            after.setdefault(pos, []).append(line)
            prepos = pos
            pos = i
            stdin.append(b('echo "\n%s %s $?"\n' % (usalt, i)))
            stdin.append(line[len(cmdline):])
        elif line.startswith(conline):
            after.setdefault(prepos, []).append(line)
            stdin.append(line[len(conline):])
        elif not line.startswith(indent):
            after.setdefault(pos, []).append(line)
    stdin.append(b('echo "\n%s %s $?"\n' % (usalt, i + 1)))

    output, retcode = execute([shell, '-'], stdin=b('').join(stdin),
                              stdout=PIPE, stderr=STDOUT, env=env)
    if retcode == 80:
        return (refout, None, [])

    # Add a trailing newline to the input script if it's missing.
    if refout and not refout[-1].endswith(b('\n')):
        refout[-1] += b('\n')

    # We use str.split instead of splitlines to get consistent
    # behavior between Python 2 and 3. In 3, we use unicode strings,
    # which has more line breaks than \n and \r.
    pos = -1
    ret = 0
    for i, line in enumerate(output[:-1].split(b('\n'))):
        line += b('\n')
        if line.startswith(salt):
            presalt = postout.pop()
            if presalt != indent + b('\n'):
                postout.append(presalt[:-1] + b(' (no-eol)\n'))
            ret = int(line.split()[2])
            if ret != 0:
                postout.append(indent + b('[%s]\n' % (ret)))
            postout += after.pop(pos, [])
            pos = int(line.split()[1])
        else:
            if _needescape(line):
                line = _escape(line)
            postout.append(indent + line)
    postout += after.pop(pos, [])

    if testname:
        diffpath = testname
        errpath = diffpath + b('.err')
    else:
        diffpath = errpath = b('')
    diff = unified_diff(refout, postout, diffpath, errpath,
                        matchers=[glob, regex])
    for firstline in diff:
        return refout, postout, itertools.chain([firstline], diff)
    return refout, postout, []

def testfile(path, shell, indent=2, env=None, cleanenv=True):
    """Run test at path and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].

    Note that the TESTDIR and TESTFILE environment variables will be
    available to use in the test.
    """
    f = open(path, 'rb')
    try:
        abspath = os.path.abspath(path)
        env = env or os.environ.copy()
        env['TESTDIR'] = fsdecode(os.path.dirname(abspath))
        env['TESTFILE'] = fsdecode(os.path.basename(abspath))
        testname = os.path.basename(abspath)
        return test(f, shell, indent=indent, testname=testname, env=env,
                    cleanenv=cleanenv)
    finally:
        f.close()
