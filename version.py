from pathlib import Path

import tomli
import tomli_w

BASEPATH = Path(__file__).parent.resolve()
PY_PROJECT_FILE = BASEPATH / "pyproject.toml"


def pyproject():
    with open(PY_PROJECT_FILE, "r") as f:
        return f.read()


def current_version():
    config = tomli.loads(pyproject())
    version = config["tool"]["poetry"]["version"]
    major, minor, patch = (int(part) for part in version.split("."))
    return major, minor, patch


def bump_version(major, minor, patch):
    config = tomli.loads(pyproject())
    major, minor, patch = current_version()
    with open(PY_PROJECT_FILE, "wb") as f:
        config["tool"]["poetry"]["version"] = f"{major}.{minor}.{patch}"
        tomli_w.dump(config, f)
        return major, minor, patch
