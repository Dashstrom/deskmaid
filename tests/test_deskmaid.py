"""Test config."""

import os
import shutil
from pathlib import Path
from typing import Iterable, Tuple

import pytest

from deskmaid import Deskmaid
from tests.utils import list_files


@pytest.mark.parametrize(
    "path",
    [
        ("a.txt", ("a.txt", "a (1).txt"), "a (2).txt"),
        ("b.test.txt", ("b.test (1).txt", "b.test.txt"), "b.test (2).txt"),
        ("c.test.txt", ("c (1).test.txt", "c.test.txt"), "c.test (1).txt"),
        ("d.tar.gz", ("d.tar.gz", "d (1).tar.gz"), "d (2).tar.gz"),
        ("e", ("e", "e (1)"), "e (2)"),
        (".txt", (".txt", "(1).txt"), "(2).txt"),
        ("f (1).txt", ("f (1).txt",), "f (1) (1).txt"),
    ],
)
def test_rename(
    deskmaid: Deskmaid,
    tmp_path: Path,
    path: Tuple[str, Iterable[str], str],
) -> None:
    """Check if renaming is correct."""
    shutil.rmtree(tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)

    for name in path[1]:
        (tmp_path / name).touch()
    src = tmp_path / path[0]
    expected = tmp_path / path[2]
    assert deskmaid.rename(src) == expected


def test_arrange(deskmaid: Deskmaid) -> None:
    """Check if arrange do well the things."""
    desktop = deskmaid.config.desktop.render()
    (desktop / "test.txt").touch()
    (desktop / "test.csv").touch()
    deskmaid.organize()
    storage = deskmaid.config.storage.render()
    paths = list_files(storage)
    assert not list_files(desktop), "Some files are not arranged"
    assert {"texts/test.txt", "data/test.csv"} == paths, "Wrong places"


def test_undo(deskmaid: Deskmaid) -> None:
    """Check if arrange do well the things."""
    desktop = deskmaid.config.desktop.render()
    (desktop / "test.txt").touch()
    (desktop / "test.csv").touch()
    (desktop / "test.lnk").touch()
    before = list_files(desktop)
    deskmaid.organize()
    deskmaid.config.storage.render()
    assert list_files(desktop) == {"test.lnk"}
    deskmaid.undo()
    after = list_files(desktop)
    assert before == after


@pytest.mark.skipif(
    os.name != "nt",
    reason="Shortcut is only implemented on Windows",
)
def test_shortcut(deskmaid: Deskmaid) -> None:
    """Check if arrange do well the things."""
    desktop = deskmaid.config.desktop.render()
    deskmaid.shortcut()
    app = f"{deskmaid.config.title}.lnk"
    files = "Files.lnk"
    assert list_files(desktop) == {app, files}
