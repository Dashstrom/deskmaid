"""Configuration for all tests."""

import pathlib
from typing import Any, Dict

import msgspec
import pytest

from deskmaid import __author__
from deskmaid.config import Config, TemplatePath
from deskmaid.deskmaid import Deskmaid
from deskmaid.file import get_root_directory


@pytest.fixture(autouse=True)
def _add_author(doctest_namespace: Dict[str, Any]) -> None:
    """Update doctest namespace."""
    doctest_namespace["author"] = __author__


@pytest.fixture()
def resources() -> pathlib.Path:
    """Get resources folder."""
    return pathlib.Path(__file__).parent / "tests" / "resources"


@pytest.fixture()
def config() -> Config:
    """Get config."""
    path = get_root_directory() / "config" / "config.yml"
    content = path.read_bytes()
    return msgspec.yaml.decode(content, type=Config)


@pytest.fixture()
def deskmaid(tmp_path: pathlib.Path) -> Deskmaid:
    """Get config."""
    deskmaid = Deskmaid.load(dry_run=True)
    desktop = tmp_path / "desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    deskmaid.config.desktop = TemplatePath(str(desktop))
    deskmaid.config.storage = TemplatePath(str(tmp_path / "storage"))
    deskmaid.config.storage = TemplatePath(
        str(tmp_path / "cache" / "latest.jsonl"),
    )
    return deskmaid
