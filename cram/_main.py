"""Main entry point"""

import configparser
import optparse
import os
import shlex
import shutil
import sys
import tempfile
from abc import ABC
from collections.abc import Callable
from typing import cast

from cram._cli import runcli
from cram._run import runtests
from cram._xunit import runxunit

__all__ = ['main']

class _Options(ABC):
    """Abstract class to give parsed options type hinting (via casting)"""

    version: bool
    quiet: bool
    verbose: bool
    interactive: bool
    debug: bool
    yes: bool
    no: bool
    preserve_env: bool
    keep_tmpdir: bool
    shell: str
    shell_opts: str | None
    indent: int
    xunit_file: str | None

class _OptionParser(optparse.OptionParser):
    """Parses command line, CRAM=, and .cramrc options"""

    def __init__(self, usage: str, prog: str) -> None:
        self._config_opts: dict[str, bool] = {}
        super().__init__(usage=usage, prog=prog)

    def _add_config_opt(self, option: optparse.Option) -> None:
        if option.dest and option.dest != 'version':
            key = option.dest.replace('_', '-')
            self._config_opts[key] = option.action == 'store_true'

    def add(self, opt_str: str, /, *opts: str | None, action: str | None=None,
            dest: str | None=None, default: str | None=None,
            help: str | None=None, # ruff: ignore[builtin-argument-shadowing]
            metavar: str | None=None) -> optparse.Option:
        option = super().add_option(opt_str, *opts, action=action, dest=dest,
                                    default=default, help=help,
                                    metavar=metavar)
        self._add_config_opt(option)
        return option

    def add_int(self, opt_str: str, /, *opts: str | None,
            action: str | None=None, dest: str | None=None,
            default: int | None=None,
            help: str | None=None, # ruff: ignore[builtin-argument-shadowing]
            metavar: str | None=None) -> optparse.Option:
        option = super().add_option(opt_str, *opts, action=action, type='int',
                                    dest=dest, default=default, help=help,
                                    metavar=metavar)
        self._add_config_opt(option)
        return option

    def parse(self, args: list[str] | None=None,
              ) -> tuple[optparse.Values, list[str]]:
        config = configparser.RawConfigParser()
        config.read(os.path.expanduser(os.environ.get('CRAMRC', '.cramrc')))
        defaults: dict[str, bool | str] = {}
        for key, isbool in self._config_opts.items():
            try:
                if isbool:
                    try:
                        defaults[key] = config.getboolean('cram', key)
                    except ValueError:
                        self.error(f'--{key}: invalid boolean value: '
                                   f'{config.get("cram", key)!r}')
                else:
                    defaults[key] = config.get('cram', key)
            except ( # ruff: ignore[try-except-in-loop]
                    configparser.NoSectionError, configparser.NoOptionError):
                pass
        self.set_defaults(**defaults)

        eargs = os.environ.get('CRAM', '').strip()
        if eargs:
            args = args or []
            args += shlex.split(eargs)

        try:
            return super().parse_args(args)
        except optparse.OptionValueError:
            self.error(str(sys.exc_info()[1]))

def _parseopts(args: list[str]) -> tuple[_Options, list[str],
                                         Callable[[], str]]:
    """Parse command line arguments"""
    p = _OptionParser(usage='cram [OPTIONS] TESTS...', prog='cram')
    p.add('-V', '--version', action='store_true',
          help='show version information and exit')
    p.add('-q', '--quiet', action='store_true',
          help="don't print diffs")
    p.add('-v', '--verbose', action='store_true',
          help='show filenames and test status')
    p.add('-i', '--interactive', action='store_true',
          help='interactively merge changed test output')
    p.add('-d', '--debug', action='store_true',
          help='write script output directly to the terminal')
    p.add('-y', '--yes', action='store_true',
          help='answer yes to all questions')
    p.add('-n', '--no', action='store_true',
          help='answer no to all questions')
    p.add('-E', '--preserve-env', action='store_true',
          help="don't reset common environment variables")
    p.add('--keep-tmpdir', action='store_true',
          help='keep temporary directories')
    p.add('--shell', action='store', default='/bin/sh', metavar='PATH',
          help='shell to use for running tests (default: %default)')
    p.add('--shell-opts', action='store', metavar='OPTS',
          help='arguments to invoke shell with')
    p.add_int('--indent', action='store', default=2, metavar='NUM',
              help=('number of spaces to use for indentation '
                    '(default: %default)'))
    p.add('--xunit-file', action='store', metavar='PATH',
          help='path to write xUnit XML output')
    opts, args = cast('tuple[_Options, list[str]]', p.parse(args))
    return opts, args, p.get_usage

def main(args: list[str]) -> int:
    """Run cram.

    If you're thinking of using Cram in other Python code (e.g., unit tests),
    consider using the test() or testfile() functions instead.

    :param args: Script arguments (excluding script name)
    :type args: str
    :return: Exit code (non-zero on failure)
    :rtype: int
    """
    opts, paths, getusage = _parseopts(args)
    if opts.version:
        sys.stdout.write("""Cram CLI testing framework (version 0.8)

Copyright (C) 2010-2025 aiiie and others
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
""")
        return 0

    conflicts = [('--yes', opts.yes, '--no', opts.no),
                 ('--quiet', opts.quiet, '--interactive', opts.interactive),
                 ('--debug', opts.debug, '--quiet', opts.quiet),
                 ('--debug', opts.debug, '--interactive', opts.interactive),
                 ('--debug', opts.debug, '--verbose', opts.verbose),
                 ('--debug', opts.debug, '--xunit-file', opts.xunit_file)]
    for s1, o1, s2, o2 in conflicts:
        if o1 and o2:
            sys.stderr.write(f'options {s1} and {s2} are '
                             'mutually exclusive\n')
            return 2

    shellcmd = shutil.which(opts.shell)
    if not shellcmd:
        sys.stderr.write(f'shell not found: {opts.shell}\n')
        return 2
    shell = [shellcmd]
    if opts.shell_opts:
        shell += shlex.split(opts.shell_opts)

    patchcmd = None
    if opts.interactive:
        patchcmd = shutil.which('patch')
        if not patchcmd:
            sys.stderr.write('patch(1) required for -i\n')
            return 2

    if not paths:
        sys.stdout.write(getusage())
        return 2

    badpath = next((p for p in paths if not os.path.exists(p)), None)
    if badpath is not None:
        sys.stderr.write(f'no such file: {badpath}\n')
        return 2

    if opts.yes:
        answer = 'y'
    elif opts.no:
        answer = 'n'
    else:
        answer = None

    tmpdir = tempfile.mkdtemp('', 'cramtests-')
    os.environ['CRAMTMP'] = tmpdir
    proctmp = os.path.join(tmpdir, 'tmp')
    for s in ('TMPDIR', 'TEMP', 'TMP'):
        os.environ[s] = proctmp

    os.mkdir(proctmp)
    try:
        tests = runtests(paths, tmpdir, shell, indent=opts.indent,
                         cleanenv=not opts.preserve_env, debug=opts.debug)
        if not opts.debug:
            tests = runcli(tests, quiet=opts.quiet, verbose=opts.verbose,
                           patchcmd=patchcmd, answer=answer)
            if opts.xunit_file is not None:
                tests = runxunit(tests, opts.xunit_file)

        hastests = False
        failed = False
        for test in tests:
            hastests = True
            result = test.run()
            if result.diff is not None:
                failed = True

        if not hastests:
            sys.stderr.write('no tests found\n')
            return 2

        return int(failed)
    finally:
        if opts.keep_tmpdir:
            sys.stdout.write(f'# Kept temporary directory: {tmpdir}\n')
        else:
            shutil.rmtree(tmpdir)
