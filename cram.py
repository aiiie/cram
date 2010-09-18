"""Command line application testing framework"""

import difflib
import itertools
import os
import re
import subprocess
import sys
import time

_natsub = re.compile(r'\d+').sub
def _natkey(s):
    """Return a key usable for natural sorting.

    >>> _natkey('foo')
    'foo'
    >>> _natkey('foo1')
    'foo11'
    >>> _natkey('foo10')
    'foo210'
    """
    return _natsub(lambda i: str(len(i.group())) + i.group(), s)

def istest(path):
    """Return whether or not a file is a test.

    >>> istest('foo')
    False
    >>> istest('.foo.t')
    False
    >>> istest('foo.t')
    True
    """
    return not path.startswith('.') and path.endswith('.t')

def findtests(paths):
    """Yield tests in paths in naturally sorted order"""
    for p in sorted(paths, key=_natkey):
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                if os.path.split(root)[1].startswith('.'):
                    continue
                for f in sorted(files, key=_natkey):
                    if istest(f):
                        yield os.path.normpath(os.path.join(root, f))
        elif istest(p):
            yield os.path.normpath(p)

def _match(pattern, s):
    try:
        return re.match(pattern, s)
    except re.error:
        return False

def test(path):
    """Run test at path and return [] on success and diff on failure.

    Diffs returned are generators.
    """
    f = open(path)
    p = subprocess.Popen(['/bin/sh', '-'], bufsize=-1, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         universal_newlines=True,
                         close_fds=os.name == 'posix')
    salt = 'CRAM%s' % time.time()

    expected, after = {}, {}
    refout, postout = [], []

    pos = prepos = -1
    for i, line in enumerate(f):
        refout.append(line)
        if line.startswith('  $ '):
            after.setdefault(pos, []).append(line)
            prepos = pos
            pos = i
            p.stdin.write('echo %s %s $?\n' % (salt, i))
            p.stdin.write(line[4:])
        elif line.startswith('  > '):
            after.setdefault(prepos, []).append(line)
            p.stdin.write(line[4:])
        elif line.startswith('  '):
            expected.setdefault(pos, []).append(line[2:])
        else:
            after.setdefault(pos, []).append(line)
    p.stdin.write('echo %s %s $?\n' % (salt, i + 1))

    pos = -1
    ret = 0
    for i, line in enumerate(p.communicate()[0].splitlines(True)):
        if line.startswith(salt):
            ret = int(line.split()[2])
            if ret != 0:
                postout.append('  [%s]\n' % ret)
            postout += after.pop(pos, [])
            pos = int(line.split()[1])
        else:
            eline = None
            if expected.get(pos):
                eline = expected[pos].pop(0)

            if eline == line:
                postout.append('  ' + line)
            elif eline and _match(eline, line):
                postout.append('  ' + eline)
            else:
                postout.append('  ' + line)
    postout += after.pop(pos, [])

    diff = difflib.unified_diff(refout, postout, path, path + '.out')
    try:
        firstline = diff.next()
        return itertools.chain([firstline], diff)
    except StopIteration:
        return []

def run(paths, verbose=False):
    """Run tests in paths and yield output.

    If verbose is True, filenames and status information are yielded.
    """
    for path in findtests(paths):
        if verbose:
            yield '%s: ' % path
        if not os.stat(path).st_size:
            if verbose:
                yield 'empty\n'
        else:
            diff = test(path)
            if diff:
                if verbose:
                    yield 'failed\n'
                else:
                    yield '\n'
                for line in diff:
                    yield line
            elif verbose:
                yield 'passed\n'
        if not verbose:
            yield '.'

def main(args):
    """Main entry point.

    args should not contain the script name.
    """
    if '-h' in args or '--help' in args:
        print >> sys.stderr, 'usage: cram [-v|--verbose] [-h|--help] [TESTS]'
        return 1

    paths = [s for s in args if not s.startswith('-')] or ['.']
    verbose = '-v' in args or '--verbose' in args
    for line in run(paths, verbose):
        sys.stdout.write(line)
        sys.stdout.flush()
    if not verbose:
        print

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
