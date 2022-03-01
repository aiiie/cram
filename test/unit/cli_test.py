from collections import namedtuple
from inspect import cleandoc

import pytest

from prysk.cli import ArgumentParser, _env_args, load

Configuration = namedtuple("Configuration", ("expected", "filename", "content"))

CONFIGURATIONS = (
    Configuration(
        expected={},
        filename=".pryskrc",
        content=cleandoc(
            """[prysk]
               yes = True
    """
        ),
    ),
    Configuration(
        expected={},
        filename=".invalid_section_name_rc",
        content=cleandoc(
            """[frysk]
               yes = True
    """
        ),
    ),
)


@pytest.fixture
def config_file(tmp_path, request):
    name, content = request.param
    file = tmp_path / name
    with open(file, "w") as f:
        f.write(content)
    yield file


def test_argument_parser_collects_options():
    parser = ArgumentParser()
    parser.add_argument("-o", "--option", action="store_true")
    parser.add_argument("-i", "--iflag", action="store_true")
    parser.add_argument(
        "-f",
        "--flag",
    )

    def rule(e):
        _type, name = e
        return name

    expected = sorted(
        (
            (bool, "option"),
            (bool, "iflag"),
            (None, "flag"),
        ),
        key=rule,
    )
    assert expected == sorted(parser.options, key=rule)


@pytest.mark.parametrize(
    "config_file,expected",
    (((c.filename, c.content), c.expected) for c in CONFIGURATIONS),
    indirect=["config_file"],
)
def test_no_section_can_be_found(config_file, expected):
    c = load(config_file, [])
    assert expected == c


@pytest.mark.parametrize(
    "expected,config_file,supported_options,section",
    [
        (
            ValueError,
            (
                ".pryskrc",
                cleandoc(
                    """
                                   [prysk]
                                    yes = not_a_bool
                                    """
                ),
            ),
            ["yes"],
            "prysk",
        ),
        (
            ValueError,
            (
                ".pryskrc",
                cleandoc(
                    """
                                   [prysk]
                                    yes = 2.0
                                    """
                ),
            ),
            ["yes"],
            "prysk",
        ),
    ],
    indirect=["config_file"],
)
def test_load_config_fails_on_incompatible_types(
    expected, config_file, supported_options, section
):
    with pytest.raises(expected) as execinfo:
        config = load(config_file, supported_options, section)


@pytest.mark.parametrize(
    "var,env,expected",
    [
        ("SOME_VAR", {}, []),
        ("SOME_VAR", {"SOME_VAR": "-n -y"}, ["-n", "-y"]),
    ],
)
def test_returns_empty_list_of_args(var, env, expected):
    assert expected == _env_args(var, env)
