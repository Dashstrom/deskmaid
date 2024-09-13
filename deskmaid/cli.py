"""Module for command line interface."""

import argparse
import logging
import sys
from typing import NoReturn, Optional, Sequence

from .deskmaid import Deskmaid
from .i18n import gettext
from .info import __issues__, __summary__, __version__

LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
logger = logging.getLogger(__name__)


class HelpArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        """Handle error from argparse.ArgumentParser."""
        self.print_help(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n")


def get_parser() -> argparse.ArgumentParser:
    """Prepare ArgumentParser."""
    parser = HelpArgumentParser(
        prog="deskmaid",
        description=__summary__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s, version {__version__}",
        help=gettext("show program's version number and exit"),
    )

    # Add subparsers
    subparsers = parser.add_subparsers(
        help=gettext("desired action to perform"),
        dest="action",
        required=True,
    )

    # Add parent parser with common arguments
    parent_parser = HelpArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-v",
        "--verbose",
        help=gettext("verbose mode, enable INFO and DEBUG messages."),
        action="store_true",
        required=False,
    )

    # Parser of run command
    run_parser = subparsers.add_parser(
        "clean",
        parents=[parent_parser],
        help=gettext("run deskmaid for clean your desktop."),
    )
    run_parser.add_argument(
        "--dry-run",
        help=gettext("do not move files."),
        action="store_true",
        default=False,
        required=False,
    )
    run_parser.add_argument(
        "-r",
        "--recursive",
        help=gettext("recursive arrange."),
        action="store_true",
        default=False,
        required=False,
    )
    run_parser.add_argument(
        "--path",
        "-p",
        help=gettext("path to the directory to arrange."),
        required=False,
    )

    # Parser of undo command
    undo_parser = subparsers.add_parser(
        "undo",
        parents=[parent_parser],
        help=gettext("undo the last run command."),
    )
    undo_parser.add_argument(
        "--dry-run",
        help=gettext("do not move files."),
        action="store_true",
        default=False,
        required=False,
    )

    # Parser of shortcut command
    shortcut_parser = subparsers.add_parser(
        "shortcut",
        parents=[parent_parser],
        help=gettext("create shortcuts on desktop."),
    )
    shortcut_parser.add_argument(
        "--debug",
        help=gettext("show logs and wait before exit."),
        action="store_true",
        default=False,
        required=False,
    )
    return parser


def setup_logging(verbose: Optional[bool] = None) -> None:
    """Do setup logging."""
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    )


def entrypoint(argv: Optional[Sequence[str]] = None) -> None:
    """Entrypoint for command line interface."""
    try:
        parser = get_parser()
        args = parser.parse_args(argv)
        setup_logging(args.verbose)
        if args.action == "clean":
            maid = Deskmaid.load(dry_run=args.dry_run)
            maid.clean(
                path=args.path,
                dry_run=args.dry_run,
                recursive=args.recursive,
            )
        elif args.action == "undo":
            maid = Deskmaid.load(dry_run=args.dry_run)
            maid.undo(dry_run=args.dry_run)
        elif args.action == "shortcut":
            maid = Deskmaid.load()
            maid.shortcut(debug=args.debug)
        else:
            parser.error(gettext("No command specified"))
    except Exception as err:  # NoQA: BLE001
        logger.critical(gettext("Unexpected error"), exc_info=err)
        logger.critical(
            gettext("Please, report this error to %s."),
            __issues__,
        )
        sys.exit(1)
