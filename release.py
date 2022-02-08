import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from inspect import cleandoc
from pathlib import Path
from subprocess import CalledProcessError, run

import tomli
import tomli_w

BASEPATH = Path(__file__).parent.resolve()
PY_PROJECT_FILE = BASEPATH / "pyproject.toml"
RELEASE_NOTES = BASEPATH / "docs" / "prysk_news.rst"


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @staticmethod
    def from_string(version):
        major, minor, patch = (int(part) for part in version.split("."))
        return Version(major=major, minor=minor, patch=patch)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def _pyproject():
    with open(PY_PROJECT_FILE, "r") as f:
        return f.read()


def current_version():
    config = tomli.loads(_pyproject())
    return Version.from_string(config["tool"]["poetry"]["version"])


def bump_version(major, minor, patch):
    config = tomli.loads(_pyproject())
    with open(PY_PROJECT_FILE, "wb") as f:
        version = Version(major, minor, patch)
        config["tool"]["poetry"]["version"] = f"{version}"
        tomli_w.dump(config, f)
        return version


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--major", action="store_true", default=False, help="Bump major version"
    )
    parser.add_argument(
        "--minor", action="store_true", default=False, help="Bump minor version"
    )
    parser.add_argument(
        "--patch", action="store_true", default=False, help="Bump patch version"
    )
    return parser


def _run_tests():
    try:
        run(["python", "-m", "nox", "--stop-on-first-error"], check=True)
        return True
    except CalledProcessError:
        print("Can't release if not all checks pass", file=sys.stderr)
        return False


def _change_log(version):
    c = run(
        ["git", "--no-pager", "log", "--oneline", f"{version}..HEAD"],
        stdout=subprocess.PIPE,
        check=True,
    )

    def clean(entry):
        parts = entry.split(" ")
        return " ".join(parts[1:])

    lines = (line for line in c.stdout.decode("utf-8").split("\n") if line != "")
    return "\n".join(f"* {clean(line)}" for line in lines)


def _update_version(version, inc_major, inc_minor, inc_patch):
    major, minor, patch = version.major, version.minor, version.patch
    major += 1 if inc_major else 0
    minor += 1 if inc_minor else 0
    patch += 1 if inc_patch else 0
    return bump_version(major, minor, patch)


def _add_release_notes(release_notes, version, change_log):
    with open(release_notes, "r+") as f:
        _date = date.today()
        old_release_notes = f.read()
        f.seek(0)
        f.write(
            cleandoc(
                """
        Version {version} ({month}. {day}, {year})
        -----------------------------------------------------
        {change_log}
        
        {old_release_notes}
        """
            ).format(
                version=version,
                month=_date.strftime("%B"),
                day=_date.day,
                year=_date.year,
                change_log=change_log,
                old_release_notes=old_release_notes,
            )
        )


def _commit_new_version(version, change_log):
    commit_msg = cleandoc(
        """
    Release {version}

    {change_log}
    """
    ).format(version=version, change_log=change_log)
    run(["git", "add", f"{PY_PROJECT_FILE.resolve()}"], check=True)
    run(["git", "add", f"{RELEASE_NOTES.resolve()}"], check=True)
    run(["git", "commit", "-m", commit_msg], check=True)
    run(["git", "commit", "--amend"], check=True)


def _add_git_tag(version):
    run(["git", "tag", "-a", "-m", f"Release {version}", f"{version}"], check=True)


def _build():
    run(["poetry", "build"], check=True)


def _publish(version):
    run(["poetry", "publish"], check=True)
    run(["git", "push", "origin", f"{version}"], check=True)


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args()
    old_version = current_version()

    try:
        _run_tests()  # and build docs
        change_log = _change_log(old_version)
        new_version = _update_version(old_version, args.major, args.minor, args.patch)
        _add_release_notes(RELEASE_NOTES, new_version, change_log)
        _commit_new_version(new_version, change_log)
        _add_git_tag(new_version)
        _build()
        _publish(new_version)
        return 0
    except Exception as ex:
        print(f"{ex}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
