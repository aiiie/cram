"""The command line interface implementation"""

import os
import sys
from collections.abc import Iterable

from cram._process import execute
from cram._test import Test, TestResult

__all__ = ['runcli']

def _prompt(question: str, answers: str, auto: str | None=None) -> str:
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
        sys.stdout.write(f'{question} [{answers}] ')
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

def _log(msg: str | None=None, verbosemsg: str | None=None,
         verbose: bool=False) -> None:
    """Write msg to standard out and flush.

    If verbose is True, write verbosemsg instead.
    """
    if verbose:
        msg = verbosemsg
    if msg:
        sys.stdout.write(msg)
        sys.stdout.flush()

def _patch(cmd: str, diff: list[bytes]) -> bool:
    """Run echo [lines from diff] | cmd -p0"""
    _out, retcode = execute([cmd, '-p0'], stdin=b''.join(diff))
    return retcode == 0

def runcli(tests: Iterable[Test], quiet: bool=False, verbose: bool=False,
           patchcmd: str | None=None, answer: str | None=None
           ) -> Iterable[Test]:
    """Run tests with command line interface input/output.

    This function yields a new sequence where each test function is wrapped
    with a function that handles CLI input/output.

    If quiet is True, diffs aren't printed. If verbose is True,
    filenames and status information are printed.

    If patchcmd is set, a prompt is written to stdout asking if
    changed output should be merged back into the original test. The
    answer is read from stdin. If 'y', the test is patched using patch
    based on the changed output.
    """
    total = skipped = failed = 0

    for path, run in tests:
        def runwrapper() -> TestResult:
            nonlocal total, skipped, failed
            """Test function that adds CLI output"""
            total += 1
            _log(None, f'{path}: ', verbose)

            refout, postout, diff = run()
            if refout is None:
                skipped += 1
                _log('s', 'empty\n', verbose)
                return TestResult(refout, postout, diff)

            abspath = os.path.abspath(path)
            errpath = abspath + '.err'

            if postout is None:
                skipped += 1
                _log('s', 'skipped\n', verbose)
            elif not diff is not None:
                _log('.', 'passed\n', verbose)
                if os.path.exists(errpath):
                    os.remove(errpath)
            else:
                failed += 1
                _log('!', 'failed\n', verbose)
                if not quiet:
                    _log('\n', None, verbose)

                with open(errpath, 'wb') as errfile:
                    errfile.writelines(postout)

                if not quiet:
                    diffout: list[bytes] = []
                    for line in diff:
                        sys.stdout.buffer.write(line)
                        diffout.append(line)
                    diff = diffout

                    if (patchcmd and
                        _prompt('Accept this change?', 'yN', answer) == 'y'):
                        if _patch(patchcmd, diff):
                            _log(None, f'{path}: merged output\n', verbose)
                            os.remove(errpath)
                        else:
                            _log(f'{path}: merge failed\n')

            return TestResult(refout, postout, diff or None)

        yield Test(path, runwrapper)

    if total > 0:
        _log('\n', None, verbose)
        _log(f'# Ran {total} tests, {skipped} skipped, {failed} failed.\n')
