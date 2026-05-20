"""Utilities for running subprocesses"""

import subprocess # ruff: ignore[suspicious-subprocess-import]
from collections.abc import Mapping
from enum import Enum
from typing import Literal

__all__ = ['ErrMode', 'OutMode', 'execute']

class OutMode(Enum):
    """Sentinel type for subprocess.PIPE"""

    PIPE = subprocess.PIPE

class ErrMode(Enum):
    """Sentinel type for subprocess.STDOUT"""

    STDOUT = subprocess.STDOUT

def execute(args: list[str], stdin: bytes | None=None,
            stdout: Literal[OutMode.PIPE] | None=None,
            stderr: Literal[ErrMode.STDOUT] | None=None,
            cwd: bytes | None=None, env: Mapping[str, str] | None=None
            ) -> tuple[bytes, int]:
    """Run a process and return its output and return code.

    stdin may either be None or a string to send to the process.

    stdout may either be None or OutMode.PIPE. If set to OutMode.PIPE, the
    process's output is returned as a byte string.

    stderr may either be None or ErrMode.STDOUT. If stdout is set to
    OutMode.PIPE and stderr is set to ErrMode.STDOUT, the process's stderr
    output will be interleaved with stdout and returned as a byte string.

    cwd sets the process's current working directory.

    env can be set to a dictionary to override the process's environment
    variables.

    This function returns a 2-tuple of (output, returncode).
    """
    pstdout = subprocess.PIPE if stdout is OutMode.PIPE else None
    pstderr = subprocess.STDOUT if stderr is ErrMode.STDOUT else None
    p = subprocess.Popen( # ruff: ignore[subprocess-without-shell-equals-true]
                         args, stdin=subprocess.PIPE, stdout=pstdout,
                         stderr=pstderr, cwd=cwd, env=env, bufsize=-1)
    ret: tuple[bytes, bytes] = p.communicate(stdin)
    return ret[0], p.returncode
