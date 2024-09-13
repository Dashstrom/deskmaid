"""Build package."""

from pathlib import Path

import babel.messages.frontend

ROOT_DIR = Path(__file__).parent
PO_DIR = ROOT_DIR / "deskmaid" / "locale"


def create_mo_files() -> None:
    cli = babel.messages.frontend.CommandLineInterface()
    cli.run(["pybabel", "compile", "--directory", str(PO_DIR)])  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    create_mo_files()
