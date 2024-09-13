"""Main module."""

from .cli import entrypoint
from .deskmaid import Deskmaid
from .info import (
    __author__,
    __email__,
    __license__,
    __maintainer__,
    __summary__,
    __version__,
)

__all__ = [
    "entrypoint",
    "Deskmaid",
    "__author__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__summary__",
    "__version__",
]
