from pathlib import Path

from prysk.run import _findtests, cwd


def create_directory(root, name):
    _dir = Path(root) / name
    _dir.mkdir()
    return _dir


def create_file(directory, name, data):
    file = Path(directory) / name
    file.touch()
    with open(file, "w") as f:
        f.write(data)
    return file


def test_findtests_ignores_hidden_file_in_current_directory(tmpdir):
    file = create_file(tmpdir, "default.t", "")
    expected = (Path(file.name),)
    with cwd(tmpdir):
        assert tuple(_findtests([file.name])) == expected


def test_findtests_ignores_hidden_files(tmpdir):
    _ = create_file(tmpdir, ".hidden.t", "")
    visible_file = create_file(tmpdir, "visible.t", "")
    expected = (visible_file,)
    assert tuple(_findtests([tmpdir])) == expected


def test_findtests_ignores_folders(tmpdir):
    hidden_directory = create_directory(tmpdir, ".hidden")
    _ = create_file(hidden_directory, "visible.t", "")
    expected = tuple()
    assert tuple(_findtests([tmpdir])) == expected
