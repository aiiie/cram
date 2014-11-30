"""Utilities for diffing test files and their output"""

import difflib
import re

__all__ = ['glob', 'regex', 'unified_diff']

def _regex(pattern, s):
    """Match a regular expression or return False if invalid.

    >>> [bool(_regex(r, 'foobar')) for r in ('foo.*', '***')]
    [True, False]
    """
    try:
        return re.match(pattern + r'\Z', s)
    except re.error:
        return False

def _glob(el, l):
    r"""Match a glob-like pattern.

    The only supported special characters are * and ?. Escaping is
    supported.

    >>> bool(_glob(r'\* \\ \? fo?b*', '* \\ ? foobar'))
    True
    """
    i, n = 0, len(el)
    res = ''
    while i < n:
        c = el[i]
        i += 1
        if c == '\\' and el[i] in '*?\\':
            res += el[i - 1:i + 1]
            i += 1
        elif c == '*':
            res += '.*'
        elif c == '?':
            res += '.'
        else:
            res += re.escape(c)
    return _regex(res, l)

def _matchannotation(keyword, matchfunc, el, l):
    """Apply match function based on annotation keyword"""
    ann = ' (%s)\n' % keyword
    return el.endswith(ann) and matchfunc(el[:-len(ann)], l[:-1])

def regex(el, l):
    """Apply a regular expression match to a line annotated with '(re)'"""
    return _matchannotation('re', _regex, el, l)

def glob(el, l):
    """Apply a glob match to a line annotated with '(glob)'"""
    return _matchannotation('glob', _glob, el, l)

class _SequenceMatcher(difflib.SequenceMatcher, object):
    """Like difflib.SequenceMatcher, but supports custom match functions"""
    def __init__(self, *args, **kwargs):
        self._matchers = kwargs.pop('matchers', [])
        super(_SequenceMatcher, self).__init__(*args, **kwargs)

    def _match(self, el, l):
        """Tests for matching lines using custom matchers"""
        for matcher in self._matchers:
            if matcher(el, l):
                return True
        return False

    def find_longest_match(self, alo, ahi, blo, bhi):
        """Find longest matching block in a[alo:ahi] and b[blo:bhi]"""
        # SequenceMatcher uses find_longest_match() to slowly whittle down
        # the differences between a and b until it has each matching block.
        # Because of this, we can end up doing the same matches many times.
        matches = []
        for n, (el, line) in enumerate(zip(self.a[alo:ahi], self.b[blo:bhi])):
            if el != line and self._match(el, line):
                # This fools the superclass's method into thinking that the
                # regex/glob in a is identical to b by replacing a's line (the
                # expected output) with b's line (the actual output).
                self.a[alo + n] = line
                matches.append((n, el))
        ret = super(_SequenceMatcher, self).find_longest_match(alo, ahi,
                                                               blo, bhi)
        # Restore the lines replaced above. Otherwise, the diff output
        # would seem to imply that the tests never had any regexes/globs.
        for n, el in matches:
            self.a[alo + n] = el
        return ret

def unified_diff(a, b, fromfile='', tofile='', fromfiledate='',
                 tofiledate='', n=3, lineterm='\n', matchers=[]):
    """Compare two sequences of lines; generate the delta as a unified diff.

    This is like difflib.unified_diff(), but allows custom matchers.
    """
    started = False
    matcher = _SequenceMatcher(None, a, b, matchers=matchers)
    for group in matcher.get_grouped_opcodes(n):
        if not started:
            fromdate = fromfiledate and '\t%s' % fromfiledate or ''
            todate = fromfiledate and '\t%s' % tofiledate or ''
            yield '--- %s%s%s' % (fromfile, fromdate, lineterm)
            yield '+++ %s%s%s' % (tofile, todate, lineterm)
            started = True
        i1, i2, j1, j2 = group[0][1], group[-1][2], group[0][3], group[-1][4]
        yield "@@ -%d,%d +%d,%d @@%s" % (i1 + 1, i2 - i1, j1 + 1, j2 - j1,
                                         lineterm)
        for tag, i1, i2, j1, j2 in group:
            if tag == 'equal':
                for line in a[i1:i2]:
                    yield ' ' + line
                continue
            if tag == 'replace' or tag == 'delete':
                for line in a[i1:i2]:
                    yield '-' + line
            if tag == 'replace' or tag == 'insert':
                for line in b[j1:j2]:
                    yield '+' + line
