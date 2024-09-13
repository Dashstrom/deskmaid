"""Locales."""

import gettext as _gettext
import locale
import os
import pathlib
from typing import Union

Translation = Union[_gettext.GNUTranslations, _gettext.NullTranslations]


def load_translations() -> Translation:
    """Load translations."""
    locale_path = str(pathlib.Path(__file__).parent / "locale")
    try:
        translation: Translation = _gettext.translation(
            "messages", localedir=locale_path
        )
    except FileNotFoundError:
        if os.name == "nt":
            import ctypes

            windll = ctypes.windll.kernel32
            lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
            os.environ["LANG"] = lang
        translation = _gettext.translation(
            "messages",
            localedir=locale_path,
            fallback=True,
        )
    translation.install()
    _gettext.bindtextdomain("messages", localedir=locale_path)
    _gettext.textdomain("messages")
    return translation


_translation = load_translations()
gettext = _translation.gettext
ngettext = _translation.ngettext
