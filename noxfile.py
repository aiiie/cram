import tempfile
from pathlib import Path

import nox

BASEPATH = Path(__file__).parent.resolve()

nox.options.sessions = [
    "isort",
    "code_format",
    "pylint",
    "integration",
    "coverage",
]


def _prepare(session):
    session.env["PYTHONPATH"] = f"{BASEPATH}"
    with tempfile.TemporaryDirectory() as tmp:
        requirements = Path(tmp) / "requirements.txt"
        session.run_always(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "-o",
            f"{requirements}",
            silent=True,
            external=True,
        )
        session.install(f"-r{requirements}")
    session.install(f"{BASEPATH}")


@nox.session
def code_format(session):
    _prepare(session)
    session.run(
        "python",
        "-m",
        "black",
        "--check",
        "--diff",
        "--color",
        f"{BASEPATH}",
    )


@nox.session
def isort(session):
    _prepare(session)
    session.run("python", "-m", "isort", "-v", "--check", f"{BASEPATH}")


@nox.session
def pylint(session):
    _prepare(session)
    session.run("python", "-m", "pylint", f'{BASEPATH / "prysk"}')
    session.run("python", "-m", "pylint", f'{BASEPATH / "scripts"}')


@nox.session
@nox.parametrize("shell", ["dash", "bash", "zsh"])
def integration(session, shell):
    session.install(f"{BASEPATH}")
    session.env["TESTOPTS"] = f"--shell={shell}"
    session.run(
        "prysk", f"--shell={shell}", f'{BASEPATH / "test" / "integration" / "prysk"}'
    )


@nox.session
def coverage(session):
    _prepare(session)
    session.env["COVERAGE"] = "coverage"
    session.env["COVERAGE_FILE"] = f'{BASEPATH / ".coverage"}'
    command = [
        "coverage",
        "run",
        "-a",
        f'--rcfile={BASEPATH / ".coveragerc"}',
        "-m",
        "prysk.cli",
    ]
    session.run(
        *(command + ["--shell=bash", f'{BASEPATH / "test" / "integration" / "prysk"}'])
    )
    session.run(
        *(command + ["--shell=dash", f'{BASEPATH / "test" / "integration" / "prysk"}'])
    )
    session.run(
        *(command + ["--shell=zsh", f'{BASEPATH / "test" / "integration" / "prysk"}'])
    )
    session.run("coverage", "report", "--fail-under=97")
    session.run("coverage", "lcov")


@nox.session
def docs(session):
    _prepare(session)
    session.run("make", "-C", f'{BASEPATH / "docs"}', "html")
