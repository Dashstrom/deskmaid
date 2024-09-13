"""Config for deskmaid."""

import logging
import pathlib
import re
import shutil
from pathlib import Path
from typing import Any, Dict, Match, Optional, Set, Type

from msgspec import Struct, field, json, yaml

from .file import get_config_directory, get_root_directory
from .i18n import gettext

logger = logging.getLogger(__name__)


class TemplateString:
    __slots__ = ("_template",)

    _RE_PATTERN = re.compile(
        r"(?P<before>[^\{]|)\{(?P<variable>[^\}]+)\}(?P<after>[^\}]|)"
    )

    def __init__(self, template: str) -> None:
        """Template for str."""
        self._template = template

    def render(self, **variables: Any) -> str:
        """Render the template with provided variables."""

        def repl(match: Match[str]) -> str:
            var = match["variable"]
            return (
                match["before"] + str(variables.get(var, var)) + match["after"]
            )

        return self._RE_PATTERN.sub(repl, self._template)


class TemplatePath:
    __slots__ = ("_template",)

    def __init__(self, template: str) -> None:
        """Template for path."""
        self._template = TemplateString(template)

    def render(self, **variables: Any) -> Path:
        """Render the template with provided variables."""
        return Path(
            self._template.render(
                root=get_root_directory(),
                home=Path.home(),
                **variables,
            )
        )


class FilterConfig(Struct, kw_only=True, forbid_unknown_fields=True):
    extensions: Set[str] = field(default_factory=set)
    files: Set[str] = field(default_factory=set)
    headers: Set[str] = field(default_factory=set)


def dec_hook(type: Type[Any], value: Any) -> Any:  # noqa: A002
    """Decode hook for msgspec."""
    if type is TemplateString:
        return TemplateString(value)
    if type is TemplatePath:
        return TemplatePath(value)
    if type is pathlib.Path:
        return pathlib.Path(value)
    error_message = gettext("Invalid type %(type)r for %(value)r") % {
        "type": type,
        "value": value,
    }
    raise ValueError(error_message)


def enc_hook(value: Any) -> Any:
    """Decode hook for msgspec."""
    if isinstance(value, TemplateString):
        return str(value)
    if isinstance(value, TemplatePath):
        return str(value)
    if isinstance(value, pathlib.Path):
        return str(value)
    error_message = gettext("Invalid type %(type)r for %(value)r") % {
        "type": type(value),
        "value": value,
    }
    raise ValueError(error_message)


class Move(Struct, kw_only=True, forbid_unknown_fields=True):
    src: Path
    dst: Path

    def do(self, dry_run: Optional[bool] = None) -> None:
        """Move the file."""
        logger.info(gettext("Move %s to %s"), self.src, self.dst)
        if not dry_run:
            self.dst.parent.mkdir(exist_ok=True, parents=True)
            shutil.move(str(self.src), str(self.dst))

    def undo(self, dry_run: Optional[bool] = None) -> None:
        """Undo the move."""
        logger.info(gettext("Undo %s to %s"), self.src, self.dst)
        if not dry_run:
            self.src.parent.mkdir(exist_ok=True, parents=True)
            shutil.move(str(self.dst), str(self.src))

    @staticmethod
    def load(line: bytes) -> "Move":
        """Load Move from bytes."""
        return json.decode(line, dec_hook=dec_hook, type=Move)

    def dump(self) -> bytes:
        """Dump Move into bytes."""
        return json.encode(self, enc_hook=enc_hook) + b"\n"


class Config(Struct, kw_only=True, forbid_unknown_fields=True):
    desktop: TemplatePath
    storage: TemplatePath
    filters: Dict[str, FilterConfig]
    fallback: str
    title: str
    app_icon: TemplatePath
    storage_icon: TemplatePath
    ignore: FilterConfig = field(default_factory=FilterConfig)
    history: TemplatePath

    @staticmethod
    def load(
        path: Optional[Path] = None,
        dry_run: Optional[bool] = None,
    ) -> "Config":
        """Load config from path or create it."""
        if path is None:
            if dry_run:
                path = get_root_directory() / "config" / "config.yml"
            else:
                path = get_config_directory() / "config.yml"
                if not path.exists():
                    template = get_root_directory() / "config" / "config.yml"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(template, path)
        content = path.read_bytes()
        return yaml.decode(content, type=Config, dec_hook=dec_hook)
