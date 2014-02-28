"""Utilities for running subprocesses"""

import os
import signal
import subprocess
import sys

__all__ = ['PIPE', 'STDOUT', 'popen']

PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT

def _makeresetsigpipe():
    """Make a function to reset SIGPIPE to SIG_DFL (for use in subprocesses).

    Doing subprocess.Popen(..., preexec_fn=makeresetsigpipe()) will prevent
    Python's SIGPIPE handler (SIG_IGN) from being inherited by the
    child process.
    """
    if sys.platform == 'win32' or getattr(signal, 'SIGPIPE', None) is None:
        return None
    return lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def popen(args, stdin=None, stdout=None, stderr=None, cwd=None, env=None):
    """Create a new subprocess.Popen instance.

    This sets up proper/consistent handling of subprocesses.
    """
    return subprocess.Popen(args, stdin=stdin, stdout=stdout, stderr=stderr,
                            cwd=cwd, env=env, bufsize=-1,
                            universal_newlines=True,
                            preexec_fn=_makeresetsigpipe(),
                            close_fds=os.name == 'posix')
