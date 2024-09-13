"""Script for arrange desktop.

Use `config.yml` for options
"""

import logging
import os
import shlex
import sys
from collections import defaultdict
from io import BytesIO
from pathlib import Path
from time import sleep
from typing import IO, Dict, Optional

from plyer import notification

from .config import Config, Move
from .file import PathLike, split_filename, to_path
from .i18n import gettext, ngettext

logger = logging.getLogger(__name__)


class Deskmaid:
    def __init__(self, config: Config) -> None:
        """Instanciate deskmaid."""
        self.config = config

    @staticmethod
    def load(
        path: Optional[Path] = None,
        dry_run: Optional[bool] = None,
    ) -> "Deskmaid":
        """Load config from path or default location."""
        return Deskmaid(Config.load(path, dry_run=dry_run))

    def organize(  # noqa: C901, PLR0912
        self,
        *,
        path: Optional[PathLike] = None,
        recursive: Optional[bool] = None,
        dry_run: Optional[bool] = None,
    ) -> Dict[Path, Path]:
        """Organize all non-ignored files and return the moved files."""
        if dry_run is None:
            dry_run = False
        if recursive is None:
            recursive = False
        if path is None:
            target = self.config.desktop.render()
        else:
            target = to_path(path)
        storage = self.config.storage.render()
        if dry_run:
            storage.mkdir(parents=True, exist_ok=True)
        # Make fast mapping
        mapping = defaultdict(
            lambda: self.config.fallback,
            {
                extension.casefold(): name
                for name, filter in self.config.filters.items()  # noqa: A001
                for extension in filter.extensions
            },
        )

        # Support recursive
        iterator = target.glob("**/*") if recursive else target.iterdir()

        # Save all changes
        if dry_run:
            stream: IO[bytes] = BytesIO()
        else:
            history = self.config.history.render()
            history.parent.mkdir(parents=True, exist_ok=True)
            stream = history.open("wb")

        # Create mapping
        ignore_extensions = {
            ext.casefold() for ext in self.config.ignore.extensions
        }

        # Find all files to move and there destinations
        files: Dict[Path, Path] = {}
        with stream:
            # Iterate files with smallest files first
            for src in sorted(iterator, key=lambda p: p.stat().st_size):
                # Keep only files
                if not src.is_file():
                    continue

                # Perform intelligent separation between stem and ext
                _, ext = split_filename(src)
                if ext.startswith("."):
                    ext = ext[1:]

                # Apply filters
                if src.name in self.config.ignore.files:
                    continue
                if ext in ignore_extensions:
                    continue

                # Find destination
                directory = storage / mapping[ext]
                dst = directory / src.name

                # Deskmaid has been run on himself
                if src == dst:
                    continue

                # Move file and save it into history
                move = Move(src=src, dst=self.rename(dst))
                move.do(dry_run=dry_run)
                if not dry_run:
                    stream.write(move.dump())
                files[src] = dst
        return files

    def rename(self, path: Path) -> Path:
        """Fix filenames."""
        # CHeck if fix is required
        if not path.exists():
            return path

        name, ext = split_filename(path)

        # Iterate until find correct file
        counter = 0
        while True:
            counter += 1
            result = path.parent / f"{name} ({counter}){ext}".strip()
            if not result.exists():
                return result

    def clean(
        self,
        *,
        path: Optional[PathLike] = None,
        recursive: Optional[bool] = None,
        dry_run: Optional[bool] = None,
    ) -> None:
        """Run deskmaid."""
        self.notify(
            gettext("At your command, senpai")
            + " (\u2044 \u2044•\u2044ω\u2044•\u2044 \u2044)"
        )
        try:
            arranged = self.organize(
                path=path,
                dry_run=dry_run,
                recursive=recursive,
            )
            if arranged:
                self.notify(
                    ngettext(
                        "one files arranged",
                        "%(num)d file arranged",
                        len(arranged),
                    )
                    % {"num": len(arranged)}
                    + " ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊"
                )
            else:
                self.notify(
                    gettext(
                        "Oni-chan, everything is tidy\n"
                        "It's just the two of us now\n"
                    )
                    + "(\u2044 \u2044>\u2044 ▽ \u2044<\u2044 \u2044)"
                )
        except Exception as err:
            self.notify(str(err))
            logger.exception("An error was occurred", exc_info=err)

    def undo(self, dry_run: Optional[bool] = None) -> None:
        """Undo last arrange."""
        if dry_run is None:
            dry_run = False
        history = self.config.history.render()
        if history.exists():
            lines = history.read_bytes().strip().split(b"\n")
            for line in lines:
                move = Move.load(line)
                move.undo(dry_run=dry_run)
            history.unlink()

    def notify(self, message: str) -> bool:
        """Send desktop notification."""
        try:
            notification.notify(
                title=self.config.title,
                message=message,
                app_name=self.config.title,
                app_icon=str(self.config.app_icon.render()),
                ticker=self.config.title,
            )
            sleep(1)
        except NotImplementedError:
            logger.exception(
                gettext("Failed to send notification: %s"),
                message,
            )
            return False
        return True

    def _create_desktop_shortcut_windows(self, *, debug: bool) -> None:
        """Create shortcut on windows."""
        # Import API

        from win32com.client import CDispatch, Dispatch

        # Get desktop path
        desktop = self.config.desktop.render()

        # Load API
        shell = Dispatch("WScript.Shell")

        # Resolve path of executable
        python_exe = Path(sys.executable)
        pythonw_exe = python_exe.parent / "pythonw.exe"
        if pythonw_exe.exists() and not debug:
            python_exe = pythonw_exe

        # Resolve current module name
        module_name = vars(sys.modules[__name__])["__package__"]

        # Create program shortcut
        shortcut_path = str(desktop / f"{self.config.title}.lnk")
        lnk: CDispatch = shell.CreateShortCut(shortcut_path)
        lnk.TargetPath = str(python_exe)
        args = ["-m", module_name, "run"]
        if debug:
            args.insert(0, "-i")
            args.append("--dry-run")
            args.append("--verbose")
        lnk.Arguments = shlex.join(args)
        lnk.IconLocation = str(self.config.app_icon.render())
        lnk.save()

        # Create directory shortcut
        shortcut_path = str(desktop / "Files.lnk")
        Path(shortcut_path).unlink(missing_ok=True)
        lnk = shell.CreateShortCut(shortcut_path)
        lnk.TargetPath = str(self.config.storage.render())
        lnk.IconLocation = str(self.config.storage_icon.render())
        lnk.save()

    def shortcut(self, debug: Optional[bool] = None) -> None:
        """Create shortcut on desktop."""
        if debug is None:
            debug = False
        if os.name == "nt":
            self._create_desktop_shortcut_windows(debug=debug)
        else:
            raise NotImplementedError
