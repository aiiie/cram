import argparse

import pytest

from prysk.settings import Settings, merge_settings, settings_from


@pytest.mark.parametrize(
    "expected,obj",
    [
        (Settings(), {}),
        (Settings(yes=True), {"yes": True}),
        (
            Settings(shell_opts=["--foo", "-b", "-a", "-r"]),
            {"shell_opts": ["--foo", "-b", "-a", "-r"]},
        ),
        (
            Settings(yes=True, debug=False),
            argparse.Namespace(yes=True, debug=False),
        ),
    ],
)
def test_settings_from(expected, obj):
    assert expected == settings_from(obj)


@pytest.mark.parametrize(
    "expected,lhs,rhs",
    [
        (
            Settings(yes=True, debug=False),
            Settings(),
            Settings(yes=True, debug=False),
        ),
        (
            Settings(yes=True, debug=False),
            Settings(yes=True),
            Settings(debug=False),
        ),
        (
            Settings(yes=False, debug=True),
            Settings(yes=True, debug=False),
            Settings(yes=False, debug=True),
        ),
    ],
)
def test_merge_settings(expected, lhs, rhs):
    assert expected == merge_settings(lhs, rhs)
