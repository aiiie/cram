"""Encoding utilities"""

import os
import sys

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

__all__ = ['b', 'bchr', 'bytestype', 'envencode', 'fsdecode', 'fsencode',
           'stdoutb', 'stderrb', 'u', 'ul', 'unicodetype']

bytestype = getattr(builtins, 'bytes', str)
unicodetype = getattr(builtins, 'unicode', str)

if getattr(os, 'fsdecode', None) is not None:
    fsdecode = os.fsdecode
    fsencode = os.fsencode
elif bytestype is not str:
    if sys.platform == 'win32':
        def fsdecode(s):
            """Decode a filename from the filesystem encoding"""
            if isinstance(s, unicodetype):
                return s
            encoding = sys.getfilesystemencoding()
            if encoding == 'mbcs':
                return s.decode(encoding)
            else:
                return s.decode(encoding, 'surrogateescape')

        def fsencode(s):
            """Encode a filename to the filesystem encoding"""
            if isinstance(s, bytestype):
                return s
            encoding = sys.getfilesystemencoding()
            if encoding == 'mbcs':
                return s.encode(encoding)
            else:
                return s.encode(encoding, 'surrogateescape')
    else:
        def fsdecode(s):
            """Decode a filename from the filesystem encoding"""
            if isinstance(s, unicodetype):
                return s
            return s.decode(sys.getfilesystemencoding(), 'surrogateescape')

        def fsencode(s):
            """Encode a filename to the filesystem encoding"""
            if isinstance(s, bytestype):
                return s
            return s.encode(sys.getfilesystemencoding(), 'surrogateescape')
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
