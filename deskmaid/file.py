"""Utils directories."""

import sys
from pathlib import Path, PurePath
from typing import Tuple, Union

from .i18n import gettext


def get_root_directory() -> Path:
    """Get root directory."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # noqa: SLF001
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def get_config_directory() -> Path:
    """Get config directory."""
    return Path.home() / ".config" / "deskmaid"


PathLike = Union[str, PurePath]


def to_path(path: PathLike) -> Path:
    """Get path."""
    if isinstance(path, Path):
        return path
    if isinstance(path, PurePath):
        return Path(path)
    if isinstance(path, str):
        return Path(path)
    raise TypeError(gettext("%(path)s is not a valid path") % {"path": path})


EXTRA_EXT = ["gz", "bz2", "xz"]


def split_filename(path: Path) -> Tuple[str, str]:
    """Split name and suffix."""
    # Split extension and fix it for empty and compression
    name = path.stem
    ext = path.suffix

    # When file has two extension and one is an extra
    if ext.split(".")[-1] in EXTRA_EXT and "." in name:
        name, ext = name.rsplit(".", 1)
        ext = "." + ext + path.suffix

    # If file is like .<ext> without something before the dot
    # Use name as ext
    if not ext and "." in name:
        ext = name
        name = ""

    # Return the name and the casefold extension
    return name, ext.casefold()
