"""Utilities for running subprocesses"""

import os
import subprocess
import sys

__all__ = ['PIPE', 'STDOUT', 'execute']

PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT

def execute(args, stdin=None, stdout=None, stderr=None, cwd=None, env=None):
    """Run a process and return its output and return code.

    stdin may either be None or a string to send to the process.

    stdout may either be None or PIPE. If set to PIPE, the process's output
    is returned as a string.

    stderr may either be None or STDOUT. If stdout is set to PIPE and stderr
    is set to STDOUT, the process's stderr output will be interleaved with
    stdout and returned as a string.

    cwd sets the process's current working directory.

    env can be set to a dictionary to override the process's environment
    variables.

    This function returns a 2-tuple of (output, returncode).
    """
    if sys.platform == 'win32': # pragma: nocover
        args = [os.fsdecode(arg) for arg in args]

    p = subprocess.Popen(args, stdin=PIPE, stdout=stdout, stderr=stderr,
                         cwd=cwd, env=env, bufsize=-1,
                         close_fds=os.name == 'posix')
    out, err = p.communicate(stdin)
    return out, p.returncode
