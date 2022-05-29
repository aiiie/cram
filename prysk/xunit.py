"""xUnit XML output"""

import locale
import re
import socket
import sys
import time
from inspect import cleandoc

__all__ = ["runxunit"]

_WIDE_CDATA_REGEX = (
    r"(?:[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd" r"\U00010000-\U0010ffff]|]]>)"
)
_NARROW_CDATA_REGEX = r"(?:[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd]" r"|]]>)"
_WIDE_QUOTE_ATTR_REGEX = (
    r"[^\x20\x21\x23-\x25\x27-\x3b\x3d"
    r"\x3f-\ud7ff\ue000-\ufffd"
    r"\U00010000-\U0010ffff]"
)
_NARROW_QUOTE_ATTR_REGEX = (
    r"[^\x20\x21\x23-\x25\x27-\x3b\x3d" r"\x3f-\ud7ff\ue000-\ufffd]"
)
_REPLACEMENT_CHAR = "\N{REPLACEMENT CHARACTER}"

if sys.maxunicode >= 0x10FFFF:
    _CDATASUB = re.compile(_WIDE_CDATA_REGEX).sub
    _QUOTEATTRSUB = re.compile(_WIDE_QUOTE_ATTR_REGEX).sub
else:
    _CDATASUB = re.compile(_NARROW_CDATA_REGEX).sub
    _QUOTEATTRSUB = re.compile(_NARROW_QUOTE_ATTR_REGEX).sub


def _cdatareplace(m):
    """Replace _CDATASUB() regex match"""
    if m.group(0) == "]]>":
        return "]]>]]&gt;<![CDATA["
    else:
        return _REPLACEMENT_CHAR


def _cdata(s):
    r"""Escape a string as an XML CDATA block.

    >>> (_cdata('1<\'2\'>&"3\x00]]>\t\r\n') ==
    ...  '<![CDATA[1<\'2\'>&\"3\ufffd]]>]]&gt;<![CDATA[\t\r\n]]>')
    True
    """
    return f"<![CDATA[{_CDATASUB(_cdatareplace, s)}]]>"


def _quoteattrreplace(m):
    """Replace _QUOTEATTRSUB() regex match"""
    return {
        "\t": "&#9;",
        "\n": "&#10;",
        "\r": "&#13;",
        '"': "&quot;",
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
    }.get(m.group(0), _REPLACEMENT_CHAR)


def _quoteattr(s):
    r"""Escape a string for use as an XML attribute value.

    >>> (_quoteattr('1<\'2\'>&"3\x00]]>\t\r\n') ==
    ...  '"1&lt;\'2\'&gt;&amp;&quot;3\ufffd]]&gt;&#9;&#13;&#10;"')
    True
    """
    return f'"{_QUOTEATTRSUB(_quoteattrreplace, s)}"'


def _timestamp():
    """Return the current time in ISO 8601 format"""
    tm = time.localtime()
    if tm.tm_isdst == 1:
        tz = time.altzone
    else:
        tz = time.timezone

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", tm)
    hours = int(-tz / 60 / 60)
    minutes = int(abs(tz) / 60 % 60)
    timestamp += "%+03d:%02d" % (hours, minutes)
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

            classname = f"{path}"
            name = path.name

            if postout is None:
                skipped[0] += 1
                testcase = "\n".join(
                    [
                        f"  <testcase classname={_quoteattr(classname)}",
                        f"            name={_quoteattr(name)}",
                        f'            time="{testtime:6f}">',
                        "    <skipped/>",
                        "  </testcase>",
                        "",
                    ]
                )
            elif diff:
                failed[0] += 1
                diff = list(diff)
                diffu = "".join(
                    l.decode(locale.getpreferredencoding(), "replace") for l in diff
                )
                testcase = "\n".join(
                    [
                        f"  <testcase classname={_quoteattr(classname)}",
                        f"            name={_quoteattr(name)}",
                        f'            time="{testtime:6f}">',
                        f"    <failure>{_cdata(diffu)}</failure>",
                        "  </testcase>",
                        "",
                    ]
                )
            else:
                testcase = "\n".join(
                    [
                        f"  <testcase classname={_quoteattr(classname)}",
                        f"            name={_quoteattr(name)}",
                        f'            time="{testtime:6f}"/>',
                        "",
                    ]
                )

            testcases.append(testcase)
            return refout, postout, diff

        yield path, testwrapper

    suitetime = time.time() - suitestart
    # fmt: off
    header = cleandoc(f"""
         <?xml version="1.0" encoding="utf-8"?>
         <testsuite name="prysk"
                    tests="{total[0]}"
                    failures="{failed[0]}"
                    skipped="{skipped[0]}"
                    timestamp={_quoteattr(timestamp)}
                    hostname={_quoteattr(hostname)}
                    time="{suitetime:6f}">
    """) + "\n"
    # fmt: on
    footer = "</testsuite>\n"

    with open(xmlpath, "wb") as xmlfile:
        encoding = "utf-8"
        xmlfile.write(header.encode(encoding))
        [xmlfile.write(testcase.encode(encoding)) for testcase in testcases]
        xmlfile.write(footer.encode(encoding))
