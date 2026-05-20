#!/usr/bin/env python3
"""Runs doctests"""

import contextlib
import doctest
import os
import sys
from collections.abc import Iterable
from types import ModuleType

def _getmodules(pkgdir: str) -> Iterable[ModuleType]:
    """Import and yield modules in pkgdir"""
    for _root, dirs, files in os.walk(pkgdir):
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        for fn in files:
            if not fn.endswith('.py') or fn == '__main__.py':
                continue

            modname = fn.replace(os.sep, '.')[:-len('.py')]
            modname = modname.removesuffix('.__init__')
            modname = '.'.join(['cram', modname])
            fromlist: list[str] = ([modname.rsplit('.', 1)[1]]
                                   if '.' in modname else [])

            yield __import__(modname, {}, {}, fromlist)

def rundoctests(pkgdir: str) -> bool:
    """Run doctests in the given package directory"""
    totalfailures = totaltests = 0
    for module in _getmodules(pkgdir):
        failures, tests = doctest.testmod(module)
        totalfailures += failures
        totaltests += tests
    return totalfailures != 0

if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt):
        sys.exit(rundoctests(sys.argv[1]))
