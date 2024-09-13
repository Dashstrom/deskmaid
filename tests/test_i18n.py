"""Test internalization."""

import os
from copy import deepcopy
from unittest import mock

import pytest

from deskmaid.i18n import load_translations


@pytest.mark.skipif(
    os.name != "nt",
    reason="Resolver of language without env variable is only on Windows",
)
@mock.patch("ctypes.windll.kernel32.GetUserDefaultUILanguage")
def test_language(mock: mock.MagicMock) -> None:
    """Check if arrange do well the things."""
    previous = deepcopy(os.environ)
    os.environ.clear()
    try:
        mock.return_value = 0x040C
        trans = load_translations()
        mock.assert_called_once_with()
        assert trans.info()["language"] == "fr"
        assert os.environ["LANG"] == "fr_FR"
    finally:
        os.environ.clear()
        os.environ.update(previous)
