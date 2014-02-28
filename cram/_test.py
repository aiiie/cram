"""Utilities for running individual tests"""

import itertools
import os
import re
import time

from cram._diff import unified_diff
from cram._process import PIPE, STDOUT, popen

__all__ = ['test']

_needescape = re.compile(r'[\x00-\x09\x0b-\x1f\x7f-\xff]').search
_escapesub = re.compile(r'[\x00-\x09\x0b-\x1f\\\x7f-\xff]').sub
_escapemap = dict((chr(i), r'\x%02x' % i) for i in range(256))
_escapemap.update({'\\': '\\\\', '\r': r'\r', '\t': r'\t'})

def _escape(s):
    """Like the string-escape codec, but doesn't escape quotes"""
    return _escapesub(lambda m: _escapemap[m.group(0)], s[:-1]) + ' (esc)\n'

def test(path, shell, indent=2):
    """Run test at path and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].
    """
    indent = ' ' * indent
    cmdline = '%s$ ' % indent
    conline = '%s> ' % indent

    f = open(path)
    abspath = os.path.abspath(path)
    env = os.environ.copy()
    env['TESTDIR'] = os.path.dirname(abspath)
    env['TESTFILE'] = os.path.basename(abspath)
    p = popen([shell, '-'], stdin=PIPE, stdout=PIPE, stderr=STDOUT, env=env)
    salt = 'CRAM%s' % time.time()

    after = {}
    refout, postout = [], []
    i = pos = prepos = -1
    stdin = []
    for i, line in enumerate(f):
        refout.append(line)
        if line.startswith(cmdline):
            after.setdefault(pos, []).append(line)
            prepos = pos
            pos = i
            stdin.append('echo "\n%s %s $?"\n' % (salt, i))
            stdin.append(line[len(cmdline):])
        elif line.startswith(conline):
            after.setdefault(prepos, []).append(line)
            stdin.append(line[len(conline):])
        elif not line.startswith(indent):
            after.setdefault(pos, []).append(line)
    stdin.append('echo "\n%s %s $?"\n' % (salt, i + 1))

    output = p.communicate(input=''.join(stdin))[0]
    if p.returncode == 80:
        return (refout, None, [])

    # Add a trailing newline to the input script if it's missing.
    if refout and not refout[-1].endswith('\n'):
        refout[-1] += '\n'

    # We use str.split instead of splitlines to get consistent
    # behavior between Python 2 and 3. In 3, we use unicode strings,
    # which has more line breaks than \n and \r.
    pos = -1
    ret = 0
    for i, line in enumerate(output[:-1].split('\n')):
        line += '\n'
        if line.startswith(salt):
            presalt = postout.pop()
            if presalt != '%s\n' % indent:
                postout.append(presalt[:-1] + ' (no-eol)\n')
            ret = int(line.split()[2])
            if ret != 0:
                postout.append('%s[%s]\n' % (indent, ret))
            postout += after.pop(pos, [])
            pos = int(line.split()[1])
        else:
            if _needescape(line):
                line = _escape(line)
            postout.append(indent + line)
    postout += after.pop(pos, [])

    diffpath = os.path.basename(abspath)
    diff = unified_diff(refout, postout, diffpath, diffpath + '.err')
    for firstline in diff:
        return refout, postout, itertools.chain([firstline], diff)
    return refout, postout, []
