"""The command line interface implementation"""
import argparse
import configparser
import os
import shlex
import shutil
import sys
import tempfile
from collections import defaultdict
from functools import partial
from pathlib import Path
from shutil import which

from rich.console import Console

from prysk.process import execute
from prysk.settings import merge_settings, settings_from
from prysk.test import runtests
from prysk.xunit import runxunit

VERSION = "0.12.1"


class ExitCode:
    """Possible exit codes of prysk CLI"""

    SUCCESS = 0
    TEST_FAILED = 1
    ERROR = 2


def main(argv=None):
    """Main entry point.

    If you're thinking of using Prysk in other Python code (e.g., unit tests),
    consider using the test() or testfile() functions instead.

    :param argv: Script arguments (excluding script name)
    :type argv: iterable of strings
    :return: Exit code (non-zero on failure)
    :rtype: int
    """
    return _Cli().main(argv)


def load(config, supported, section="prysk"):
    """
    Load configuration options from a init style format config file.

    :param supported: iterable of supported options and their type which should be collected.
    :param section: which contains the options.
    """
    parser = configparser.ConfigParser()
    parser.read(config)
    dispatcher = defaultdict(
        lambda: (parser.get, "--{}: invalid value: {!r}"),
        {
            bool: (parser.getboolean, "--{}: invalid boolean value: {!r}"),
            int: (parser.getint, "--{}: invalid integer value: {!r}"),
        },
    )
    if not parser.has_section(section):
        return {}

    config = {}
    for _type, option in supported:
        if not parser.has_option(section, option):
            continue
        try:
            fetch, error_msg = dispatcher[_type]
            config[option] = fetch(section, option)
        except ValueError as ex:
            fetch, error_msg = dispatcher[_type]
            value = parser.get(section, option)
            raise ValueError(error_msg.format(option, value)) from ex
    return config


def _conflicts(settings):
    conflicts = [
        ("--yes", settings.yes, "--no", settings.no),
        ("--quiet", settings.quiet, "--interactive", settings.interactive),
        ("--debug", settings.debug, "--quiet", settings.quiet),
        ("--debug", settings.debug, "--interactive", settings.interactive),
        ("--debug", settings.debug, "--verbose", settings.verbose),
        ("--debug", settings.debug, "--xunit-file", settings.xunit_file),
    ]
    for option1, value1, option2, value2 in conflicts:
        if value1 and value2:
            return option1, option2
    return None


def _env_args(var, env=None):
    env = env if env else os.environ
    args = env.get(var, "").strip()
    return shlex.split(args)


class _ArgumentParser:
    """argparse.Argumentparser compatible argument parser.

    Allows inspection of options supported by the parser"""

    @classmethod
    def create_parser(cls):
        parser = cls(
            usage="prysk [OPTIONS] TESTS...",
            prog="prysk",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            "tests",
            metavar="TESTS",
            type=Path,
            nargs="+",
            help="Path(s) to the tests to be executed",
        )
        parser.add_argument("-V", "--version", action="version", version=VERSION)
        parser.add_argument(
            "-q", "--quiet", action="store_true", help="don't print diffs"
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="show filenames and test status",
        )
        parser.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            help="interactively merge changed test output",
        )
        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="write script output directly to the terminal",
        )
        parser.add_argument(
            "-y", "--yes", action="store_true", help="answer yes to all questions"
        )
        parser.add_argument(
            "-n", "--no", action="store_true", help="answer no to all questions"
        )
        parser.add_argument(
            "-E",
            "--preserve-env",
            action="store_true",
            help="don't reset common environment variables",
        )
        parser.add_argument(
            "--keep-tmpdir",
            action="store_true",
            help="keep temporary directories",
        )
        parser.add_argument(
            "--shell",
            action="store",
            default="/bin/sh",
            metavar="PATH",
            help="shell to use for running tests",
        )
        parser.add_argument(
            "--shell-opts",
            action="store",
            metavar="OPTS",
            help="arguments to invoke shell with",
        )
        parser.add_argument(
            "--indent",
            action="store",
            default=2,
            metavar="NUM",
            type=int,
            help="number of spaces to use for indentation",
        )
        parser.add_argument(
            "--color",
            choices=["always", "never", "auto"],
            default="auto",
            help="Mode which shall be used for coloring the output",
        )
        parser.add_argument(
            "--xunit-file",
            action="store",
            metavar="PATH",
            help="path to write xUnit XML output",
        )
        return parser

    def __init__(self, *args, **kwargs):
        self._options = []
        self._parser = argparse.ArgumentParser(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        """See argparser.Argumentparser:add_argument"""

        def is_boolean_option(a):
            return a.nargs is not None and isinstance(a.const, bool)

        action = self._parser.add_argument(*args, **kwargs)
        if not action.type:
            _type = bool if is_boolean_option(action) else None
        else:
            _type = action.type
        self._options.append((_type, action.dest))
        return action

    def __getattr__(self, item):
        return getattr(self._parser, item)

    @property
    def options(self):
        """
        Normalized options and their type except for -V, --version and -h, --help.

        :return: an iterable containing all boolean options.
        :rtype: Iterable[Tuple(type, str)]
        """
        return self._options


class _CliError(Exception):
    def __init__(self, exit_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._exit_code = exit_code

    @property
    def exit_code(self):
        return self._exit_code


class _Cli:
    @staticmethod
    def _expandpath(path):
        """Expands ~ and environment variables in path"""
        return os.path.expanduser(os.path.expandvars(path))

    @staticmethod
    def _patch(cmd, diff):
        """Run echo [lines from diff] | cmd -p0"""
        _, retcode = execute([cmd, "-p0"], stdin=b"".join(diff))
        return retcode == 0

    def __init__(self):
        self._stdout_console = Console(file=sys.stdout)
        self._stderr_console = Console(file=sys.stderr)
        self._argparser = _ArgumentParser.create_parser()
        self._default_color_system = self._stdout_console.color_system

    @property
    def stdout(self):
        return partial(
            self._stdout_console.print, no_wrap=True, overflow="ignore", crop=False
        )

    @property
    def stderr(self):
        return partial(self._stderr_console.print, no_wrap=True)

    def _color_mode(self, mode):
        dispatcher = {"auto": "auto", "never": None, "always": "standard"}
        mode = dispatcher[mode]
        self._stdout_console = Console(file=sys.stdout, color_system=mode)
        self._stderr_console = Console(file=sys.stderr, color_system=mode)

    def _log(self, msg=None, verbosemsg=None, verbose=False):
        """Write msg to standard out and flush.

        If verbose is True, write verbosemsg instead.
        """
        msg = verbosemsg if verbose else msg
        if not msg:
            return
        msg = msg.encode("utf-8") if isinstance(msg, bytes) else msg
        self.stdout(msg, end="")

    def _runcli(self, tests, quiet=False, verbose=False, patchcmd=None, answer=None):
        """Run tests with command line interface input/output.

        tests should be a sequence of 2-tuples containing the following:

            (test path, test function)

        This function yields a new sequence where each test function is wrapped
        with a function that handles CLI input/output.

        If quiet is True, diffs aren't printed. If verbose is True,
        filenames and status information are printed.

        If patchcmd is set, a prompt is written to stdout asking if
        changed output should be merged back into the original test. The
        answer is read from stdin. If 'y', the test is patched using patch
        based on the changed output.
        """
        total, skipped, failed = [0], [0], [0]

        for path, test in tests:

            def testwrapper():
                """Test function that adds CLI output"""
                total[0] += 1
                self._log(None, f"{Path(path.parent.name, path.name)}: ", verbose)

                refout, postout, diff = test()
                if refout is None:
                    skipped[0] += 1
                    self._log("[yellow]s[/yellow]", "empty\n", verbose)
                    return refout, postout, diff

                errpath = Path(f"{path}" + ".err")
                if postout is None:
                    skipped[0] += 1
                    self._log(
                        "[yellow]s[/yellow]", "[yellow]skipped[/yellow]\n", verbose
                    )
                elif not diff:
                    self._log("[green].[/green]", "[green]passed[/green]\n", verbose)
                    if errpath.exists():
                        os.remove(errpath)
                else:
                    failed[0] += 1
                    self._log("[red]![/red]", "[red]failed[/red]\n", verbose)
                    if not quiet:
                        self._log("\n", None, verbose)

                    with open(errpath, "wb") as errfile:
                        for line in postout:
                            errfile.write(line)

                    if not quiet:
                        origdiff = diff
                        diff = []
                        for line in origdiff:
                            _line = line.decode("utf-8")
                            _line = (
                                f"[green]{_line}[/green]"
                                if _line.startswith("+")
                                else _line
                            )
                            _line = (
                                f"[red]{_line}[/red]"
                                if _line.startswith("-")
                                else _line
                            )
                            _line = (
                                f"[magenta]{_line}[/magenta]"
                                if _line.startswith("@")
                                else _line
                            )
                            self.stdout(_line, end="")
                            diff.append(line)

                        if (
                            patchcmd
                            and self._prompt("Accept this change?", "yN", answer) == "y"
                        ):
                            if self._patch(patchcmd, diff):
                                self._log(None, f"{path}: merged output\n", verbose)
                                os.remove(errpath)
                            else:
                                self._log(f"{path}: merge failed\n")

                return refout, postout, diff

            yield path, testwrapper

        if total[0] > 0:
            self._log("\n", None, verbose)
            self._log(
                (
                    f"# Ran [green]{total[0]}[/green] tests, "
                    f"[yellow]{skipped[0]}[/yellow] skipped, "
                    f"[red]{failed[0]}[/red] failed.\n"
                )
            )

    def _prompt(self, question, answers, auto=None):
        """Write a prompt to stdout and ask for answer in stdin.

        answers should be a string, with each character a single
        answer. An uppercase letter is considered the default answer.

        If an invalid answer is given, this asks again until it gets a
        valid one.

        If auto is set, the question is answered automatically with the
        specified value.
        """
        default = [c for c in answers if c.isupper()]
        while True:
            self.stdout(f"{question} [[blue]{answers}[/blue]] ", end="")
            if auto is not None:
                self.stdout(auto)
                return auto

            answer = sys.stdin.readline().strip().lower()
            if not answer and default:
                return default[0]
            elif answer and answer in answers.lower():
                return answer

    def _load_settings(self, argv):
        """Loads the settings from all layers and merges them.

        Layers (Config file > ENV vars > CLI arguments)"""
        argv = sys.argv[1:] if argv is None else argv
        argv.extend(_env_args("PRYSK"))
        args = self._argparser.parse_args(argv)
        self._color_mode(args.color)
        options = self._argparser.options

        try:
            configuration_settings = settings_from(
                load(
                    Path(self._expandpath(os.environ.get("PRYSKRC", ".pryskrc"))),
                    options,
                )
            )
        except ValueError as ex:
            raise _CliError(
                ExitCode.ERROR,
                "\n".join([f"{self._argparser.format_usage()}", f"prysk: error: {ex}"]),
            ) from ex

        argument_settings = settings_from(args)
        settings = merge_settings(argument_settings, configuration_settings)
        return settings

    def main(self, argv=None):
        try:
            settings = self._load_settings(argv)
        except _CliError as ex:
            self.stderr(f"{ex}")
            return ex.exit_code

        conflict = _conflicts(settings)

        if conflict:
            arg1, arg2 = conflict
            self.stderr(f"options {arg1} and {arg2} are mutually exclusive")
            return ExitCode.ERROR

        shellcmd = which(settings.shell)
        if not shellcmd:
            self.stderr(f"shell not found: {settings.shell}")
            return ExitCode.ERROR
        shell = [shellcmd]
        if settings.shell_opts:
            shell += shlex.split(settings.shell_opts)

        patchcmd = None
        if settings.interactive:
            patchcmd = which("patch")
            if not patchcmd:
                self.stderr("patch(1) required for -i")
                return ExitCode.ERROR

        badpaths = [path for path in settings.tests if not path.exists()]
        if badpaths:
            self.stderr(f"no such file: {badpaths[0]}")
            return ExitCode.ERROR

        if settings.yes:
            answer = "y"
        elif settings.no:
            answer = "n"
        else:
            answer = None

        tmpdir = os.environ["PRYSK_TEMP"] = tempfile.mkdtemp("", "prysk-tests-")
        tmpdir = Path(tmpdir)
        proc_tmp = tmpdir / "tmp"
        for name in ("TMPDIR", "TEMP", "TMP"):
            os.environ[name] = f"{proc_tmp}"

        os.mkdir(proc_tmp)
        try:
            tests = runtests(
                settings.tests,
                tmpdir,
                shell,
                indent=settings.indent,
                cleanenv=not settings.preserve_env,
                debug=settings.debug,
            )
            if not settings.debug:
                tests = self._runcli(
                    tests,
                    quiet=settings.quiet,
                    verbose=settings.verbose,
                    patchcmd=patchcmd,
                    answer=answer,
                )
                if settings.xunit_file is not None:
                    tests = runxunit(tests, settings.xunit_file)

            hastests = False
            failed = False
            for path, test in tests:
                hastests = True
                _, _, diff = test()
                if diff:
                    failed = True

            if not hastests:
                self.stderr("[red]no tests found[/red]")
                return ExitCode.ERROR

            return ExitCode.TEST_FAILED if failed else ExitCode.SUCCESS
        finally:
            if settings.keep_tmpdir:
                self.stdout(f"# Kept temporary directory: [blue]{tmpdir}[/blue]")
            else:
                shutil.rmtree(tmpdir)
