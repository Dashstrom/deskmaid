"""Module holding metadata."""

from importlib.metadata import Distribution

from .i18n import gettext

_DISTRIBUTION = Distribution.from_name(
    "deskmaid",
)
_METADATA = _DISTRIBUTION.metadata

__author__ = _METADATA["Author"]
__email__ = _METADATA["Author-email"]
__license__ = _METADATA["License"]
__version__ = _METADATA["Version"]
__maintainer__ = _METADATA["Maintainer"]
__summary__ = gettext("Configurable desktop cleaner.")
__copyright__ = f"{__author__} <{__email__}>"
__issues__ = "https://github.com/Dashstrom/deskmaid/issues"
