from pathlib import Path

import nox

BASEPATH = Path(__file__).parent.resolve()

nox.options.sessions = [
    "isort",
    "code_format",
    "pylint",
    "unit",
    "integration",
    "coverage",
    "docs",
]


@nox.session(python=False)
def fix(session):
    session.run("poetry", "run", "python", "-m", "isort", "-v", f"{BASEPATH}")
    session.run("poetry", "run", "python", "-m", "black", f"{BASEPATH}")


@nox.session(python=False)
def code_format(session):
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "black",
        "--check",
        "--diff",
        "--color",
        f"{BASEPATH}",
    )


@nox.session(python=False)
def isort(session):
    session.run(
        "poetry", "run", "python", "-m", "isort", "-v", "--check", f"{BASEPATH}"
    )


@nox.session(python=False)
def pylint(session):
    session.run("poetry", "run", "python", "-m", "pylint", f'{BASEPATH / "prysk"}')
    session.run("poetry", "run", "python", "-m", "pylint", f'{BASEPATH / "scripts"}')


@nox.session(python=False)
def unit(session):
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "pytest",
        "--ignore-glob=prysk/*.py",
        f"{BASEPATH}",
    )


@nox.session(python=False)
@nox.parametrize("shell", ["dash", "bash", "zsh"])
def integration(session, shell):
    session.env["TESTOPTS"] = f"--shell={shell}"
    session.run(
        "poetry",
        "run",
        "prysk",
        f"--shell={shell}",
        f'{BASEPATH / "test" / "integration" / "prysk"}',
        external=True,
    )


@nox.session(python=False)
def coverage(session):
    session.env["COVERAGE"] = "coverage"
    session.env["COVERAGE_FILE"] = f'{BASEPATH / ".coverage"}'
    command = [
        "poetry",
        "run",
        "coverage",
        "run",
        "-a",
        f'--rcfile={BASEPATH / "pyproject.toml"}',
        "-m",
        "prysk",
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


@nox.session(python=False)
def docs(session):
    docs_folder = BASEPATH / "docs"
    session.run("sphinx-build", f"{docs_folder}", f'{docs_folder /  "_build" / "html"}')
