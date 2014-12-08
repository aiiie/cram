"""Encoding utilities"""

import locale
import os
import sys

__all__ = ['b', 'bchr', 'bytes_type', 'envencode', 'fsdecode', 'fsencode',
           'stdoutb', 'stderrb', 'unicode_type']

try:
    bytes
except NameError:
    bytes_type = str
    unicode_type = unicode
else:
    bytes_type = bytes
    unicode_type = str

if getattr(os, 'fsdecode', None) is not None:
    fsdecode = os.fsdecode
    fsencode = os.fsencode
elif bytes_type is not str:
    def fsdecode(s):
        if isinstance(s, unicode_type):
            return s
        return s.decode(locale.getpreferredencoding(), 'surrogateescape')

    def fsencode(s):
        if isinstance(s, bytes_type):
            return s
        return s.encode(locale.getpreferredencoding(), 'surrogateescape')
else:
    fsdecode = lambda s: s
    fsencode = lambda s: s

if bytes_type is str:
    envencode = lambda s: s
else:
    envencode = fsdecode

if getattr(sys.stdout, 'buffer', None) is not None:
    stdoutb = sys.stdout.buffer
    stderrb = sys.stderr.buffer
else:
    stdoutb = sys.stdout
    stderrb = sys.stderr

if bytes_type is str:
    b = lambda s: s
    bchr = chr
else:
    b = lambda s: s.encode('ascii')
    bchr = lambda i: bytes_type([i])
