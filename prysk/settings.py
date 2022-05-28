import argparse
from dataclasses import dataclass, field


@dataclass
class Settings:
    tests: list = field(default_factory=list)
    quiet: bool = None
    verbose: bool = None
    interactive: bool = None
    debug: bool = None
    yes: bool = None
    no: bool = None
    preserve_env: bool = None
    keep_tmpdir: bool = None
    shell: str = None
    shell_opts: list = field(default_factory=list)
    indent: int = None
    color: str = "auto"
    xunit_file: str = None


def settings_from(obj):
    supported_types = (
        argparse.Namespace,
        dict,
    )
    _class = type(obj)
    if not issubclass(_class, supported_types):
        raise TypeError(f"Can not construct settings from type: {type(obj).__name__}.")

    def from_namespace(ns):
        return Settings(**vars(ns))

    def from_dict(d):
        return Settings(**d)

    dispatcher = {
        f"{argparse.Namespace.__name__}": from_namespace,
        f"{dict.__name__}": from_dict,
    }

    return dispatcher[_class.__name__](obj)


def merge_settings(lhs, rhs):
    def items(d):
        d = vars(d)
        excludes = ["tests"]
        return ((k, v) for k, v in d.items() if k not in excludes)

    lhs_items = dict(items(lhs))
    rhs_items = dict(items(rhs))

    for name, value in rhs_items.items():
        value = value if value is not None else lhs_items.get(name, None)
        setattr(lhs, name, value)
    lhs.tests.extend(rhs.tests)
    lhs.shell_opts.extend(rhs.shell_opts)
    return lhs
