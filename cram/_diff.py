"""Utilities for diffing test files and their output"""

import codecs
import difflib
import re
from collections.abc import Callable, Iterator
from typing import TypeAlias

__all__ = ['esc', 'glob', 'regex', 'unified_diff']

def _regex(pattern: bytes, s: bytes) -> bool:
    """Match a regular expression or return False if invalid.

    >>> [_regex(r, b'foobar') for r in (b'foo.*', b'***')]
    [True, False]
    """
    try:
        return bool(re.match(pattern + br'\Z', s))
    except re.error:
        return False

def _glob(pattern: bytes, s: bytes) -> bool:
    r"""Match a glob-like pattern.

    The only supported special characters are * and ?. Escaping is
    supported.

    >>> bool(_glob(br'\* \\ \? fo?b*', b'* \\ ? foobar'))
    True
    """
    i, n = 0, len(pattern)
    res = b''
    while i < n:
        c = pattern[i:i + 1]
        i += 1
        if c == b'\\' and pattern[i] in b'*?\\':
            res += pattern[i - 1:i + 1]
            i += 1
        elif c == b'*':
            res += b'.*'
        elif c == b'?':
            res += b'.'
        else:
            res += re.escape(c)
    return _regex(res, s)

_MatchFunc: TypeAlias = Callable[[bytes, bytes], bool]

def _matchannotation(keyword: bytes, matchfunc: _MatchFunc, pattern: bytes,
                     s: bytes) -> bool:
    """Apply match function based on annotation keyword"""
    ann = b' (%s)\n' % keyword
    return pattern.endswith(ann) and matchfunc(pattern[:-len(ann)], s[:-1])

def regex(pattern: bytes, s: bytes) -> bool:
    """Apply a regular expression match to a line annotated with '(re)'"""
    return _matchannotation(b're', _regex, pattern, s)

def glob(pattern: bytes, s: bytes) -> bool:
    """Apply a glob match to a line annotated with '(glob)'"""
    return _matchannotation(b'glob', _glob, pattern, s)

def esc(pattern: bytes, s: bytes) -> bool:
    """Apply an escape match to a line annotated with '(esc)'"""
    ann = b' (esc)\n'

    if pattern.endswith(ann):
        pattern = codecs.escape_decode(pattern[:-len(ann)])[0] + b'\n'
    if pattern == s:
        return True

    if s.endswith(ann):
        s = codecs.escape_decode(s[:-len(ann)])[0] + b'\n'
    return pattern == s

class _SequenceMatcher(difflib.SequenceMatcher[bytes]):
    """Like difflib.SequenceMatcher, but supports custom match functions"""

    def __init__(self, *, a: list[bytes], b: list[bytes],
                 matchers: list[_MatchFunc] | None=None) -> None:
        self.a: list[bytes]
        self.b: list[bytes]
        self._matchers: list[_MatchFunc] = matchers or []
        super().__init__(a=a, b=b)

    def _match(self, pattern: bytes, s: bytes) -> bool:
        """Test for matching lines using custom matchers"""
        return any(m(pattern, s) for m in self._matchers)

    def find_longest_match(self, alo: int=0, ahi: int | None=None,
                           blo: int=0, bhi: int | None=None) -> difflib.Match:
        """Find longest matching block in a[alo:ahi] and b[blo:bhi]"""
        # SequenceMatcher uses find_longest_match() to slowly whittle down
        # the differences between a and b until it has each matching block.
        # Because of this, we can end up doing the same matches many times.
        matches: list[tuple[int, bytes]] = []
        for n, (el, line) in enumerate(zip(self.a[alo:ahi], self.b[blo:bhi])):
            if el != line and self._match(el, line):
                # This fools the superclass's method into thinking that the
                # regex/glob in a is identical to b by replacing a's line (the
                # expected output) with b's line (the actual output).
                self.a[alo + n] = line
                matches.append((n, el))
        ret = super().find_longest_match(alo, ahi, blo, bhi)
        # Restore the lines replaced above. Otherwise, the diff output
        # would seem to imply that the tests never had any regexes/globs.
        for n, el in matches:
            self.a[alo + n] = el
        return ret

def unified_diff(l1: list[bytes], l2: list[bytes], fromfile: bytes=b'',
                 tofile: bytes=b'', fromfiledate: bytes=b'',
                 tofiledate: bytes=b'', n: int=3, lineterm: bytes=b'\n',
                 matchers: list[_MatchFunc] | None=None) -> Iterator[bytes]:
    r"""Compare two sequences of lines; generate the delta as a unified diff.

    This is like difflib.unified_diff(), but allows custom matchers.

    >>> l1 = [b'a\n', b'? (glob)\n']
    >>> l2 = [b'a\n', b'b\n']
    >>> (list(unified_diff(l1, l2, b'f1', b'f2', b'1970-01-01',
    ...                    b'1970-01-02')) ==
    ...  [b'--- f1\t1970-01-01\n', b'+++ f2\t1970-01-02\n',
    ...   b'@@ -1,2 +1,2 @@\n', b' a\n', b'-? (glob)\n', b'+b\n'])
    True

    >>> from cram._diff import glob
    >>> list(unified_diff(l1, l2, matchers=[glob]))
    []
    """
    if matchers is None:
        matchers = []
    started = False
    matcher = _SequenceMatcher(a=l1, b=l2, matchers=matchers)
    for group in matcher.get_grouped_opcodes(n):
        if not started:
            fromdate = b'\t' + fromfiledate if fromfiledate else b''
            todate = b'\t' + tofiledate if tofiledate else b''
            yield b'--- ' + fromfile + fromdate + lineterm
            yield b'+++ ' + tofile + todate + lineterm
            started = True
        i1, i2, j1, j2 = group[0][1], group[-1][2], group[0][3], group[-1][4]
        yield (b'@@ -%d,%d +%d,%d @@' % (i1 + 1, i2 - i1, j1 + 1, j2 - j1) +
               lineterm)
        for tag, i1, i2, j1, j2 in group:
            if tag == 'equal':
                for line in l1[i1:i2]:
                    yield b' ' + line
                continue
            if tag == 'replace' or tag == 'delete':
                for line in l1[i1:i2]:
                    yield b'-' + line
            if tag == 'replace' or tag == 'insert':
                for line in l2[j1:j2]:
                    yield b'+' + line
