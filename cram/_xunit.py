"""xUnit XML output"""

import locale
import os
import re
import socket
import sys
import time
from collections.abc import Iterable

from cram._test import Test, TestResult

__all__ = ['runxunit']

_widecdataregex = (r'(?:[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd'
                   r'\U00010000-\U0010ffff]|]]>)')
_narrowcdataregex = (r'(?:[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd]'
                     r'|]]>)')
_widequoteattrregex = (r'[^\x20\x21\x23-\x25\x27-\x3b\x3d'
                       r'\x3f-\ud7ff\ue000-\ufffd'
                       r'\U00010000-\U0010ffff]')
_narrowquoteattrregex = (r'[^\x20\x21\x23-\x25\x27-\x3b\x3d'
                         r'\x3f-\ud7ff\ue000-\ufffd]')
_replacementchar = '\N{REPLACEMENT CHARACTER}'

if sys.maxunicode >= 0x10ffff: # pragma: nocover
    _cdatasub = re.compile(_widecdataregex).sub
    _quoteattrsub = re.compile(_widequoteattrregex).sub
else: # pragma: nocover
    _cdatasub = re.compile(_narrowcdataregex).sub
    _quoteattrsub = re.compile(_narrowquoteattrregex).sub

def _cdatareplace(m: re.Match[str]) -> str:
    """Replace _cdatasub() regex match"""
    if m.group(0) == ']]>':
        return ']]>]]&gt;<![CDATA['
    else:
        return _replacementchar

def _cdata(s: str) -> str:
    r"""Escape a string as an XML CDATA block.

    >>> (_cdata('1<\'2\'>&"3\x00]]>\t\r\n') ==
    ...  '<![CDATA[1<\'2\'>&\"3\ufffd]]>]]&gt;<![CDATA[\t\r\n]]>')
    True
    """
    return f'<![CDATA[{_cdatasub(_cdatareplace, s)}]]>'

def _quoteattrreplace(m: re.Match[str]) -> str:
    """Replace _quoteattrsub() regex match"""
    return {'\t': '&#9;',
            '\n': '&#10;',
            '\r': '&#13;',
            '"': '&quot;',
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;'}.get(m.group(0), _replacementchar)

def _quoteattr(s: str) -> str:
    r"""Escape a string for use as an XML attribute value.

    >>> (_quoteattr('1<\'2\'>&"3\x00]]>\t\r\n') ==
    ...  '"1&lt;\'2\'&gt;&amp;&quot;3\ufffd]]&gt;&#9;&#13;&#10;"')
    True
    """
    return f'"{_quoteattrsub(_quoteattrreplace, s)}"'

def _timestamp() -> str:
    """Return the current time in ISO 8601 format"""
    tm = time.localtime()
    tz = time.altzone if tm.tm_isdst == 1 else time.timezone
    tzhours = int(-tz / 60 / 60)
    tzmins = int(abs(tz) / 60 % 60)
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', tm)
    timestamp += f'{tzhours:+03d}:{tzmins:02d}'
    return timestamp

def runxunit(tests: Iterable[Test], xmlpath: str) -> Iterable[Test]:
    """Run tests with xUnit XML output.

    tests should be a sequence of 2-tuples containing the following:

        (test path, test function)

    This function yields a new sequence where each test function is wrapped
    with a function that writes test results to an xUnit XML file.
    """
    suitestart = time.time()
    timestamp = _timestamp()
    hostname = socket.gethostname()
    total, skipped, failed = [0], [0], [0]
    testcases: list[str] = []

    for path, run in tests:
        def testwrapper() -> TestResult:
            """Run test and collect XML output"""
            total[0] += 1

            start = time.time()
            refout, postout, diff = run()
            testtime = time.time() - start
            name = os.path.basename(path)

            if postout is None:
                skipped[0] += 1
                testcase = (f'  <testcase classname={_quoteattr(path)}\n'
                            f'            name={_quoteattr(name)}\n'
                            f'            time="{testtime:.6f}">\n'
                            '    <skipped/>\n'
                            '  </testcase>\n')
            elif diff is not None:
                failed[0] += 1
                diff = list(diff)
                diffu = ''.join(line.decode(locale.getpreferredencoding(),
                                            'replace')
                                for line in diff)
                testcase = (f'  <testcase classname={_quoteattr(path)}\n'
                            f'            name={_quoteattr(name)}\n'
                            f'            time="{testtime:.6f}">\n'
                            f'    <failure>{_cdata(diffu)}</failure>\n'
                             '  </testcase>\n')
            else:
                testcase = (f'  <testcase classname={_quoteattr(path)}\n'
                            f'            name={_quoteattr(name)}\n'
                            f'            time="{testtime:.6f}"/>\n')
            testcases.append(testcase)

            return TestResult(refout, postout, diff or None)

        yield Test(path, testwrapper)

    suitetime = time.time() - suitestart
    header = ('<?xml version="1.0" encoding="utf-8"?>\n'
              '<testsuite name="cram"\n'
              f'           tests="{total[0]:d}"\n'
              f'           failures="{failed[0]:d}"\n'
              f'           skipped="{skipped[0]:d}"\n'
              f'           timestamp={_quoteattr(timestamp)}\n'
              f'           hostname={_quoteattr(hostname)}\n'
              f'           time="{suitetime:.6f}">\n')
    footer = '</testsuite>\n'

    with open(xmlpath, 'w', encoding='utf-8') as xmlfile:
        xmlfile.write(header)
        xmlfile.writelines(testcases)
        xmlfile.write(footer)
