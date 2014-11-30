"""The test runner"""

import os
import sys

from cram._process import execute
from cram._test import test

__all__ = ['log', 'run']

def _findtests(paths):
    """Yield tests in paths in sorted order"""
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                if os.path.basename(root).startswith('.'):
                    continue
                for f in sorted(files):
                    if not f.startswith('.') and f.endswith('.t'):
                        yield os.path.normpath(os.path.join(root, f))
        else:
            yield os.path.normpath(p)

def _prompt(question, answers, auto=None):
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

def _patch(cmd, diff, path):
    """Run echo [lines from diff] | cmd -p0"""
    out, retcode = execute([cmd, '-p0'], stdin=''.join(diff), cwd=path)
    return retcode == 0

def run(paths, tmpdir, shell, quiet=False, verbose=False, patchcmd=None,
        answer=None, indent=2):
    """Run tests in paths in tmpdir.

    If quiet is True, diffs aren't printed. If verbose is True,
    filenames and status information are printed.

    If patchcmd is set, a prompt is written to stdout asking if
    changed output should be merged back into the original test. The
    answer is read from stdin. If 'y', the test is patched using patch
    based on the changed output.
    """
    cwd = os.getcwd()
    seen = set()
    basenames = set()
    skipped = failed = 0
    for i, path in enumerate(_findtests(paths)):
        abspath = os.path.abspath(path)
        if abspath in seen:
            continue
        seen.add(abspath)

        log(None, '%s: ' % path, verbose)
        if not os.stat(abspath).st_size:
            skipped += 1
            log('s', 'empty\n', verbose)
        else:
            basename = os.path.basename(path)
            if basename in basenames:
                basename = '%s-%s' % (basename, i)
            else:
                basenames.add(basename)
            testdir = os.path.join(tmpdir, basename)
            os.mkdir(testdir)
            try:
                os.chdir(testdir)
                refout, postout, diff = test(abspath, shell, indent)
            finally:
                os.chdir(cwd)

            errpath = abspath + '.err'
            if postout is None:
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
                        _prompt('Accept this change?', 'yN', answer) == 'y'):
                        if _patch(patchcmd, diff, os.path.dirname(abspath)):
                            log(None, '%s: merged output\n' % path, verbose)
                            os.remove(errpath)
                        else:
                            log('%s: merge failed\n' % path)
    log('\n', None, verbose)
    log('# Ran %s tests, %s skipped, %s failed.\n'
        % (len(seen), skipped, failed))
    return bool(failed)
