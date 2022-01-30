"""xUnit XML output"""

import locale
import os
import re
import socket
import sys
import time

__all__ = ["runxunit"]

_widecdataregex = (
    r"(?:[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd" r"\U00010000-\U0010ffff]|]]>)"
)
_narrowcdataregex = r"(?:[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd]" r"|]]>)"
_widequoteattrregex = (
    r"[^\x20\x21\x23-\x25\x27-\x3b\x3d"
    r"\x3f-\ud7ff\ue000-\ufffd"
    r"\U00010000-\U0010ffff]"
)
_narrowquoteattrregex = r"[^\x20\x21\x23-\x25\x27-\x3b\x3d" r"\x3f-\ud7ff\ue000-\ufffd]"
_replacementchar = "\N{REPLACEMENT CHARACTER}"

if sys.maxunicode >= 0x10FFFF:
    _cdatasub = re.compile(_widecdataregex).sub
    _quoteattrsub = re.compile(_widequoteattrregex).sub
else:
    _cdatasub = re.compile(_narrowcdataregex).sub
    _quoteattrsub = re.compile(_narrowquoteattrregex).sub


def _cdatareplace(m):
    """Replace _cdatasub() regex match"""
    if m.group(0) == "]]>":
        return "]]>]]&gt;<![CDATA["
    else:
        return _replacementchar


def _cdata(s):
    r"""Escape a string as an XML CDATA block.

    >>> (_cdata('1<\'2\'>&"3\x00]]>\t\r\n') ==
    ...  '<![CDATA[1<\'2\'>&\"3\ufffd]]>]]&gt;<![CDATA[\t\r\n]]>')
    True
    """
    return "<![CDATA[%s]]>" % _cdatasub(_cdatareplace, s)


def _quoteattrreplace(m):
    """Replace _quoteattrsub() regex match"""
    return {
        "\t": "&#9;",
        "\n": "&#10;",
        "\r": "&#13;",
        '"': "&quot;",
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
    }.get(m.group(0), _replacementchar)


def _quoteattr(s):
    r"""Escape a string for use as an XML attribute value.

    >>> (_quoteattr('1<\'2\'>&"3\x00]]>\t\r\n') ==
    ...  '"1&lt;\'2\'&gt;&amp;&quot;3\ufffd]]&gt;&#9;&#13;&#10;"')
    True
    """
    return '"%s"' % _quoteattrsub(_quoteattrreplace, s)


def _timestamp():
    """Return the current time in ISO 8601 format"""
    tm = time.localtime()
    if tm.tm_isdst == 1:
        tz = time.altzone
    else:
        tz = time.timezone

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", tm)
    tzhours = int(-tz / 60 / 60)
    tzmins = int(abs(tz) / 60 % 60)
    timestamp += "%+03d:%02d" % (tzhours, tzmins)
    return timestamp


def runxunit(tests, xmlpath):
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
    testcases = []

    for path, test in tests:

        def testwrapper():
            """Run test and collect XML output"""
            total[0] += 1

            start = time.time()
            refout, postout, diff = test()
            testtime = time.time() - start

            classname = path.decode(locale.getpreferredencoding(), "replace")
            name = os.path.basename(classname)

            if postout is None:
                skipped[0] += 1
                testcase = (
                    "  <testcase classname=%(classname)s\n"
                    "            name=%(name)s\n"
                    '            time="%(time).6f">\n'
                    "    <skipped/>\n"
                    "  </testcase>\n"
                ) % {
                    "classname": _quoteattr(classname),
                    "name": _quoteattr(name),
                    "time": testtime,
                }
            elif diff:
                failed[0] += 1
                diff = list(diff)
                diffu = "".join(
                    l.decode(locale.getpreferredencoding(), "replace") for l in diff
                )
                testcase = (
                    "  <testcase classname=%(classname)s\n"
                    "            name=%(name)s\n"
                    '            time="%(time).6f">\n'
                    "    <failure>%(diff)s</failure>\n"
                    "  </testcase>\n"
                ) % {
                    "classname": _quoteattr(classname),
                    "name": _quoteattr(name),
                    "time": testtime,
                    "diff": _cdata(diffu),
                }
            else:
                testcase = (
                    "  <testcase classname=%(classname)s\n"
                    "            name=%(name)s\n"
                    '            time="%(time).6f"/>\n'
                ) % {
                    "classname": _quoteattr(classname),
                    "name": _quoteattr(name),
                    "time": testtime,
                }
            testcases.append(testcase)

            return refout, postout, diff

        yield path, testwrapper

    suitetime = time.time() - suitestart
    header = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<testsuite name="prysk"\n'
        '           tests="%(total)d"\n'
        '           failures="%(failed)d"\n'
        '           skipped="%(skipped)d"\n'
        "           timestamp=%(timestamp)s\n"
        "           hostname=%(hostname)s\n"
        '           time="%(time).6f">\n'
    ) % {
        "total": total[0],
        "failed": failed[0],
        "skipped": skipped[0],
        "timestamp": _quoteattr(timestamp),
        "hostname": _quoteattr(hostname),
        "time": suitetime,
    }
    footer = "</testsuite>\n"

    xmlfile = open(xmlpath, "wb")
    try:
        xmlfile.write(header.encode("utf-8"))
        for testcase in testcases:
            xmlfile.write(testcase.encode("utf-8"))
        xmlfile.write(footer.encode("utf-8"))
    finally:
        xmlfile.close()
