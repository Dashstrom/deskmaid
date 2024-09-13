"""Test module for test on Windows and Linux."""

from pathlib import Path, PurePosixPath
from typing import Set

from deskmaid.file import PathLike


def list_files(root: PathLike) -> Set[str]:
    """List all files as linux path."""
    return {
        str(PurePosixPath(path.relative_to(root)))
        for path in Path(root).glob("**/*")
        if path.is_file()
    }
