"""The test runner"""

import os
import sys

from cram._encoding import b, bytes_type, stdoutb
from cram._process import execute
from cram._test import testfile

__all__ = ['run']

def _findtests(paths):
    """Yield tests in paths in sorted order"""
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                if os.path.basename(root).startswith(b('.')):
                    continue
                for f in sorted(files):
                    if not f.startswith(b('.')) and f.endswith(b('.t')):
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

def _log(msg=None, verbosemsg=None, verbose=False):
    """Write msg to standard out and flush.

    If verbose is True, write verbosemsg instead.
    """
    if verbose:
        msg = verbosemsg
    if msg:
        if isinstance(msg, bytes_type):
            stdoutb.write(msg)
        else:
            sys.stdout.write(msg)
        sys.stdout.flush()

def _patch(cmd, diff, path):
    """Run echo [lines from diff] | cmd -p0"""
    out, retcode = execute([cmd, '-p0'], stdin=b('').join(diff), cwd=path)
    return retcode == 0

def _runtests(paths, tmpdir, shell, indent=2, cleanenv=True):
    """Run tests and yield results.

    This yields a sequence of 3-tuples containing the following:

        (test path, absolute test path, test function)

    The test function, when called, runs the test in a temporary directory
    and returns a 3-tuple:

        (list of lines in the test, same list with actual output, diff)
    """
    cwd = os.getcwd()
    seen = set()
    basenames = set()
    for i, path in enumerate(_findtests(paths)):
        abspath = os.path.abspath(path)
        if abspath in seen:
            continue
        seen.add(abspath)

        if not os.stat(abspath).st_size:
            yield (path, abspath, None)
            continue

        basename = os.path.basename(path)
        if basename in basenames:
            basename = basename + b('-%s' % i)
        else:
            basenames.add(basename)

        def test():
            testdir = os.path.join(tmpdir, basename)
            os.mkdir(testdir)
            try:
                os.chdir(testdir)
                return testfile(abspath, shell, indent=indent,
                                cleanenv=cleanenv)
            finally:
                os.chdir(cwd)

        yield (path, abspath, test)

def run(paths, tmpdir, shell, quiet=False, verbose=False, patchcmd=None,
        answer=None, indent=2, cleanenv=True):
    """Run tests in paths in tmpdir.

    If quiet is True, diffs aren't printed. If verbose is True,
    filenames and status information are printed.

    If patchcmd is set, a prompt is written to stdout asking if
    changed output should be merged back into the original test. The
    answer is read from stdin. If 'y', the test is patched using patch
    based on the changed output.
    """
    total = skipped = failed = 0
    for path, abspath, test in _runtests(paths, tmpdir, shell, indent=indent,
                                         cleanenv=cleanenv):
        total += 1
        _log(None, path + b(': '), verbose)
        if test is None:
            skipped += 1
            _log('s', 'empty\n', verbose)
            continue

        refout, postout, diff = test()
        errpath = abspath + b('.err')

        if postout is None:
            skipped += 1
            _log('s', 'skipped\n', verbose)
        elif not diff:
            _log('.', 'passed\n', verbose)
            if os.path.exists(errpath):
                os.remove(errpath)
        else:
            failed += 1
            _log('!', 'failed\n', verbose)
            if not quiet:
                _log('\n', None, verbose)

            errfile = open(errpath, 'wb')
            try:
                for line in postout:
                    errfile.write(line)
            finally:
                errfile.close()

            if not quiet:
                if patchcmd:
                    diff = list(diff)
                for line in diff:
                    stdoutb.write(line)

                if (patchcmd and
                    _prompt('Accept this change?', 'yN', answer) == 'y'):
                    if _patch(patchcmd, diff, os.path.dirname(abspath)):
                        _log(None, path + b(': merged output\n'), verbose)
                        os.remove(errpath)
                    else:
                        _log(path + b(': merge failed\n'))
    _log('\n', None, verbose)
    _log('# Ran %s tests, %s skipped, %s failed.\n'
         % (total, skipped, failed))
    return bool(failed)
