"""Encoding utilities"""

import locale
import os
import sys

__all__ = ['b', 'bchr', 'bytestype', 'envencode', 'fsdecode', 'fsencode',
           'stdoutb', 'stderrb', 'u', 'ul', 'unicodetype']

try:
    bytes
except NameError:
    bytestype = str
    unicodetype = unicode
else:
    bytestype = bytes
    unicodetype = str

if getattr(os, 'fsdecode', None) is not None:
    fsdecode = os.fsdecode
    fsencode = os.fsencode
elif bytestype is not str:
    def fsdecode(s):
        if isinstance(s, unicodetype):
            return s
        return s.decode(locale.getpreferredencoding(), 'surrogateescape')

    def fsencode(s):
        if isinstance(s, bytestype):
            return s
        return s.encode(locale.getpreferredencoding(), 'surrogateescape')
else:
    fsdecode = lambda s: s
    fsencode = lambda s: s

if bytestype is str:
    envencode = lambda s: s
else:
    envencode = fsdecode

if getattr(sys.stdout, 'buffer', None) is not None:
    stdoutb = sys.stdout.buffer
    stderrb = sys.stderr.buffer
else:
    stdoutb = sys.stdout
    stderrb = sys.stderr

if bytestype is str:
    b = lambda s: s
    bchr = chr
    u = lambda s: s.decode('ascii')
else:
    b = lambda s: s.encode('ascii')
    bchr = lambda i: bytestype([i])
    u = lambda s: s

try:
    eval(r'u""')
except SyntaxError:
    ul = lambda e: eval(e)
else:
    ul = lambda e: eval('u' + e)
