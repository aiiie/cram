import pytest

from release import Version


@pytest.mark.parametrize(
    "data,expected",
    [
        ("1.1.0", Version(1, 1, 0)),
        ("0.0.1", Version(0, 0, 1)),
        ("0.10.2", Version(0, 10, 2)),
    ],
)
def test_from_string(data, expected):
    assert expected == Version.from_string(data)


@pytest.mark.parametrize(
    "version,expected",
    [
        (Version(1, 1, 0), "1.1.0"),
        (Version(0, 0, 1), "0.0.1"),
        (Version(0, 10, 2), "0.10.2"),
    ],
)
def test_to_string(version, expected):
    assert expected == f"{version}"
