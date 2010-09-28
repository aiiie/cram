#!/usr/bin/env python
"""Functional testing framework for command line applications"""

import difflib
import itertools
import os
import re
import subprocess
import sys
import shutil
import time
import tempfile

__all__ = ['main', 'test']

def findtests(paths):
    """Yield tests in paths in sorted order"""
    istest = lambda p: not p.startswith('.') and p.endswith('.t')
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                if os.path.basename(root).startswith('.'):
                    continue
                for f in sorted(files):
                    if istest(f):
                        yield os.path.normpath(os.path.join(root, f))
        elif istest(os.path.basename(p)):
            yield os.path.normpath(p)

def match(pattern, s):
    """Match pattern or return False if invalid.

    >>> [bool(match(r, 'foobar')) for r in ('foo.*', '***')]
    [True, False]
    """
    try:
        return re.match(pattern, s)
    except re.error:
        return False

def glob(el, l):
    """Match a glob-like pattern.

    The only supported special characters are * and ?. Escaping is
    supported.

    >>> bool(glob(r'\* \\ \? fo?b*', '* \\ ? foobar'))
    True
    """
    i, n = 0, len(el)
    res = ''
    while i < n:
        c = el[i]
        i += 1
        if c == '\\' and el[i] in '*?\\':
            res += el[i - 1:i + 1]
            i += 1
        elif c == '*':
            res += '.*'
        elif c == '?':
            res += '.'
        else:
            res += re.escape(c)
    return match(res, l)

class SequenceMatcher(difflib.SequenceMatcher, object):
    """Like difflib.SequenceMatcher, but matches globs and regexes"""

    def find_longest_match(self, alo, ahi, blo, bhi):
        """Find longest matching block in a[alo:ahi] and b[blo:bhi]"""
        # SequenceMatcher uses find_longest_match() to slowly whittle down
        # the differences between a and b until it has each matching block.
        # Because of this, we can end up doing the same matches many times.
        matches = []
        for n, (el, line) in enumerate(zip(self.a[alo:ahi], self.b[blo:bhi])):
            if (el.endswith(" (re)\n") and match(el[:-6] + '\n', line) or
                el.endswith(" (glob)\n") and glob(el[:-8] + '\n', line)):
                # This fools the superclass's method into thinking that the
                # regex/glob in a is identical to b by replacing a's line (the
                # expected output) with b's line (the actual output).
                self.a[alo + n] = line
                matches.append((n, el))
        ret = super(SequenceMatcher, self).find_longest_match(alo, ahi,
                                                              blo, bhi)
        # Restore the lines replaced above. Otherwise, the diff output
        # would seem to imply that the tests never had any regexes/globs.
        for n, el in matches:
            self.a[alo + n] = el
        return ret

def unified_diff(a, b, fromfile='', tofile='', fromfiledate='',
                 tofiledate='', n=3, lineterm='\n', matcher=SequenceMatcher):
    """Compare two sequences of lines; generate the delta as a unified diff.

    This is like difflib.unified_diff(), but allows custom matchers.
    """
    started = False
    for group in matcher(None, a, b).get_grouped_opcodes(n):
        if not started:
            fromdate = fromfiledate and '\t%s' % fromfiledate or ''
            todate = fromfiledate and '\t%s' % tofiledate or ''
            yield '--- %s%s%s' % (fromfile, fromdate, lineterm)
            yield '+++ %s%s%s' % (tofile, todate, lineterm)
            started = True
        i1, i2, j1, j2 = group[0][1], group[-1][2], group[0][3], group[-1][4]
        yield "@@ -%d,%d +%d,%d @@%s" % (i1 + 1, i2 - i1, j1 + 1, j2 - j1,
                                         lineterm)
        for tag, i1, i2, j1, j2 in group:
            if tag == 'equal':
                for line in a[i1:i2]:
                    yield ' ' + line
                continue
            if tag == 'replace' or tag == 'delete':
                for line in a[i1:i2]:
                    yield '-' + line
            if tag == 'replace' or tag == 'insert':
                for line in b[j1:j2]:
                    yield '+' + line

def test(path):
    """Run test at path and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].
    """
    f = open(path)
    abspath = os.path.abspath(path)
    env = os.environ.copy()
    env['TESTDIR'] = os.path.dirname(abspath)
    p = subprocess.Popen(['/bin/sh', '-'], bufsize=-1, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         universal_newlines=True, env=env,
                         close_fds=os.name == 'posix')
    salt = 'CRAM%s' % time.time()

    after = {}
    refout, postout = [], []

    i = pos = prepos = -1
    for i, line in enumerate(f):
        refout.append(line)
        if line.startswith('  $ '):
            after.setdefault(pos, []).append(line)
            prepos = pos
            pos = i
            p.stdin.write('echo "\n%s %s $?"\n' % (salt, i))
            p.stdin.write(line[4:])
        elif line.startswith('  > '):
            after.setdefault(prepos, []).append(line)
            p.stdin.write(line[4:])
        elif not line.startswith('  '):
            after.setdefault(pos, []).append(line)
    p.stdin.write('echo "\n%s %s $?"\n' % (salt, i + 1))

    output = p.communicate()[0]
    if p.returncode == 80:
        return (refout, None, [])

    pos = -1
    ret = 0
    for i, line in enumerate(output.splitlines(True)):
        if line.startswith(salt):
            presalt = postout.pop()
            if presalt != '  \n':
                postout.append(presalt[:-1] + '%\n')
            ret = int(line.split()[2])
            if ret != 0:
                postout.append('  [%s]\n' % ret)
            postout += after.pop(pos, [])
            pos = int(line.split()[1])
        else:
            postout.append('  ' + line)
    postout += after.pop(pos, [])

    diff = unified_diff(refout, postout, abspath, abspath + '.err')
    for firstline in diff:
        return refout, postout, itertools.chain([firstline], diff)
    return refout, postout, []

def prompt(question, answers, auto=None):
    """Write a prompt to stdout and ask for answer in stdin.

    answers should be a string, with each character a single
    answer. An uppercase letter is considered the default answer.

    If an invalid answer is given, this asks again until it gets a
    valid one.

    If auto is set, the question is answered automatically with the
    specified value.
    """
    default = [c for c in answers if c.isupper()]
    while True:
        sys.stdout.write('%s [%s] ' % (question, answers))
        sys.stdout.flush()
        if auto is not None:
            sys.stdout.write(auto + '\n')
            sys.stdout.flush()
            return auto

        answer = sys.stdin.readline().strip().lower()
        if not answer and default:
            return default[0]
        elif answer and answer in answers.lower():
            return answer

def log(msg=None, verbosemsg=None, verbose=False):
    """Write msg to standard out and flush.

    If verbose is True, write verbosemsg instead.
    """
    if verbose:
        msg = verbosemsg
    if msg:
        sys.stdout.write(msg)
        sys.stdout.flush()

def patch(cmd, diff):
    """Run echo [lines from diff] | cmd -p0"""
    p = subprocess.Popen([cmd, '-p0'], bufsize=-1, stdin=subprocess.PIPE,
                         universal_newlines=True, close_fds=os.name == 'posix')
    for line in diff:
        p.stdin.write(line)
    p.stdin.close()
    p.wait()
    return p.returncode == 0

def run(paths, quiet=False, verbose=False, basetmp=None, keeptmp=False,
        patchcmd=None, answer=None):
    """Run tests in paths.

    If quiet is True, diffs aren't printed. If verbose is True,
    filenames and status information are printed.

    If basetmp is set, each test is run in a random temporary
    directory inside basetmp. If keeptmp is also True, temporary
    directories are preserved after use.

    If patchcmd is set, a prompt is written to stdout asking if
    changed output should be merged back into the original test. The
    answer is read from stdin. If 'y', the test is patched using patch
    based on the changed output.
    """
    cwd = os.getcwd()
    seen = set()
    skipped = 0
    failed = 0
    for path in findtests(paths):
        abspath = os.path.abspath(path)
        if abspath in seen:
            continue
        seen.add(abspath)

        log(None, '%s: ' % path, verbose)
        if not os.stat(abspath).st_size:
            skipped += 1
            log('s', 'empty\n', verbose)
        else:
            if basetmp:
                tmpdir = os.path.join(basetmp, os.path.basename(path))
                os.mkdir(tmpdir)
            try:
                if basetmp:
                    os.chdir(tmpdir)
                refout, postout, diff = test(abspath)
            finally:
                if basetmp:
                    os.chdir(cwd)
                    if not keeptmp:
                        shutil.rmtree(tmpdir)

            errpath = abspath + '.err'
            if not postout:
                skipped += 1
                log('s', 'skipped\n', verbose)
            elif not diff:
                log('.', 'passed\n', verbose)
                if os.path.exists(errpath):
                    os.remove(errpath)
            else:
                failed += 1
                log('!', 'failed\n', verbose)
                if not quiet:
                    log('\n', None, verbose)
                errfile = open(errpath, 'w')
                try:
                    for line in postout:
                        errfile.write(line)
                finally:
                    errfile.close()
                if not quiet:
                    if patchcmd:
                        diff = list(diff)
                    for line in diff:
                        log(line)
                    if (patchcmd and
                        prompt('Accept this change?', 'yN', answer) == 'y'):
                        if patch(patchcmd, diff):
                            log(None, '%s: merged output\n' % path, verbose)
                            os.remove(errpath)
                        else:
                            log('%s: merge failed\n' % path)
    log('\n', None, verbose)
    log('# Ran %s tests, %s skipped, %s failed.\n'
        % (len(seen), skipped, failed))
    return bool(failed)

def which(cmd):
    """Return the patch to cmd or None if not found"""
    for p in os.environ['PATH'].split(os.pathsep):
        path = os.path.join(p, cmd)
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    return None

def main(args):
    """Main entry point.

    args should not contain the script name.
    """
    from optparse import OptionParser

    p = OptionParser(usage='cram [OPTIONS] TESTS...')
    p.add_option('-V', '--version', action='store_true',
                 help='show version information and exit')
    p.add_option('-q', '--quiet', action='store_true',
                 help="don't print diffs")
    p.add_option('-v', '--verbose', action='store_true',
                 help='show filenames and test status')
    p.add_option('-i', '--interactive', action='store_true',
                 help='interactively merge changed test output')
    p.add_option('-y', '--yes', action='store_true',
                 help='answer yes to all questions')
    p.add_option('-n', '--no', action='store_true',
                 help='answer no to all questions')
    p.add_option('--keep-tmpdir', action='store_true',
                 help='keep temporary directories')
    p.add_option('-E', action='store_false', dest='sterilize', default=True,
                 help="don't reset common environment variables")
    opts, paths = p.parse_args(args)

    if opts.version:
        sys.stdout.write("""Cram CLI testing framework (version 0.4)

Copyright (C) 2010 Brodie Rao <brodie@bitheap.org> and others
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
""")
        return

    conflicts = [('-y', opts.yes, '-n', opts.no),
                 ('-q', opts.quiet, '-v', opts.verbose),
                 ('-q', opts.quiet, '-i', opts.interactive)]
    for s1, o1, s2, o2 in conflicts:
        if o1 and o2:
            sys.stderr.write('options %s and %s are mutually exclusive\n'
                             % (s1, s2))
            return 2

    patchcmd = None
    if opts.interactive:
        patchcmd = which('patch')
        if not patchcmd:
            sys.stderr.write('patch(1) required for -i\n')
            return 2

    if not paths:
        sys.stdout.write(p.get_usage())
        return 2

    badpaths = [p for p in paths if not os.path.exists(p)]
    if badpaths:
        sys.stderr.write('no such file: %s\n' % badpaths[0])
        return 2

    basetmp = os.environ['CRAMTMP'] = tempfile.mkdtemp('', 'cramtests-')
    proctmp = os.path.join(basetmp, 'tmp')
    os.mkdir(proctmp)
    for s in ('TMPDIR', 'TEMP', 'TMP'):
        os.environ[s] = proctmp

    if opts.sterilize:
        for s in ('LANG', 'LC_ALL', 'LANGUAGE'):
            os.environ[s] = 'C'
        os.environ['TZ'] = 'GMT'
        os.environ['CDPATH'] = ''
        os.environ['COLUMNS'] = '80'
        os.environ['GREP_OPTIONS'] = ''

    if opts.yes:
        answer = 'y'
    elif opts.no:
        answer = 'n'
    else:
        answer = None

    try:
        return run(paths, opts.quiet, opts.verbose, basetmp, opts.keep_tmpdir,
                   patchcmd, answer)
    finally:
        if not opts.keep_tmpdir:
            shutil.rmtree(basetmp)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
