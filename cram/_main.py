"""Main entry point"""

import optparse
import os
import shutil
import sys
import tempfile

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from cram._run import run

def _which(cmd):
    """Return the patch to cmd or None if not found"""
    for p in os.environ['PATH'].split(os.pathsep):
        path = os.path.join(p, cmd)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return os.path.abspath(path)
    return None

def _expandpath(path):
    """Expands ~ and environment variables in path"""
    return os.path.expanduser(os.path.expandvars(path))

class _OptionParser(optparse.OptionParser):
    """Like optparse.OptionParser, but supports setting values through
    CRAM= and .cramrc."""

    def __init__(self, *args, **kwargs):
        self._config_opts = {}
        optparse.OptionParser.__init__(self, *args, **kwargs)

    def add_option(self, *args, **kwargs):
        option = optparse.OptionParser.add_option(self, *args, **kwargs)
        if option.dest and option.dest != 'version':
            key = option.dest.replace('_', '-')
            self._config_opts[key] = option.action == 'store_true'
        return option

    def parse_args(self, args=None, values=None):
        config = configparser.RawConfigParser()
        config.read(_expandpath(os.environ.get('CRAMRC', '.cramrc')))
        defaults = {}
        for key, isbool in self._config_opts.items():
            try:
                if isbool:
                    try:
                        value = config.getboolean('cram', key)
                    except ValueError:
                        value = config.get('cram', key)
                        self.error('--%s: invalid boolean value: %r'
                                   % (key, value))
                else:
                    value = config.get('cram', key)
            except (configparser.NoSectionError, configparser.NoOptionError):
                pass
            else:
                defaults[key] = value
        self.set_defaults(**defaults)

        eargs = os.environ.get('CRAM', '').strip()
        if eargs:
            import shlex
            args = args or []
            args += shlex.split(eargs)

        try:
            return optparse.OptionParser.parse_args(self, args, values)
        except optparse.OptionValueError:
            self.error(str(sys.exc_info()[1]))

def _parseopts(args):
    """Parse command line arguments"""
    p = _OptionParser(usage='cram [OPTIONS] TESTS...', prog='cram')
    p.add_option('-V', '--version', action='store_true',
                 help='show version information and exit')
    p.add_option('-q', '--quiet', action='store_true',
                 help="don't print diffs")
    p.add_option('-v', '--verbose', action='store_true',
                 help='show filenames and test status')
    p.add_option('-i', '--interactive', action='store_true',
                 help='interactively merge changed test output')
    p.add_option('-y', '--yes', action='store_true',
                 help='answer yes to all questions')
    p.add_option('-n', '--no', action='store_true',
                 help='answer no to all questions')
    p.add_option('-E', '--preserve-env', action='store_true',
                 help="don't reset common environment variables")
    p.add_option('--keep-tmpdir', action='store_true',
                 help='keep temporary directories')
    p.add_option('--shell', action='store', default='/bin/sh', metavar='PATH',
                 help='shell to use for running tests')
    p.add_option('--indent', action='store', default=2, metavar='NUM',
                 type='int', help='number of spaces to use for indentation')
    opts, paths = p.parse_args(args)
    getusage = lambda: p.get_usage()
    return opts, paths, getusage

def main(args):
    """Main entry point.

    args should not contain the script name.
    """
    opts, paths, getusage = _parseopts(args)
    if opts.version:
        sys.stdout.write("""Cram CLI testing framework (version 0.6)

Copyright (C) 2010-2014 Brodie Rao <brodie@bitheap.org> and others
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
""")
        return

    conflicts = [('-y', opts.yes, '-n', opts.no),
                 ('-q', opts.quiet, '-i', opts.interactive)]
    for s1, o1, s2, o2 in conflicts:
        if o1 and o2:
            sys.stderr.write('options %s and %s are mutually exclusive\n'
                             % (s1, s2))
            return 2

    patchcmd = None
    if opts.interactive:
        patchcmd = _which('patch')
        if not patchcmd:
            sys.stderr.write('patch(1) required for -i\n')
            return 2

    if not paths:
        sys.stdout.write(getusage())
        return 2

    badpaths = [path for path in paths if not os.path.exists(path)]
    if badpaths:
        sys.stderr.write('no such file: %s\n' % badpaths[0])
        return 2

    if opts.yes:
        answer = 'y'
    elif opts.no:
        answer = 'n'
    else:
        answer = None

    tmpdir = os.environ['CRAMTMP'] = tempfile.mkdtemp('', 'cramtests-')
    proctmp = os.path.join(tmpdir, 'tmp')
    for s in ('TMPDIR', 'TEMP', 'TMP'):
        os.environ[s] = proctmp

    os.mkdir(proctmp)
    try:
        return run(paths, tmpdir, opts.shell, opts.quiet, opts.verbose,
                   patchcmd, answer, opts.indent, not opts.preserve_env)
    finally:
        if opts.keep_tmpdir:
            sys.stdout.write('# Kept temporary directory: %s\n' % tmpdir)
        else:
            shutil.rmtree(tmpdir)

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        pass
