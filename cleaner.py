"""
Script for arrange desktop
Use a `config.yml` for options
"""

import os
import yaml
import sys
import shutil

from traceback import print_exc


# load config.yml
if getattr(sys, 'frozen', False):
    PATH = os.path.dirname(sys.executable)
else:
    PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(PATH, "config.yml")) as file_config:
    CONFIG = yaml.safe_load(file_config)

BUREAU = os.path.join("C:/Users", os.getlogin(), "Desktop")
OUTPUT = CONFIG["OUTPUT"]
IGNORE_EXTENSIONS = set(CONFIG["IGNORE EXTENSIONS"])
IGNORE_FILES = set(CONFIG["IGNORE FILES"])
EXT_OUTPUT = {ext.lower(): os.path.join(OUTPUT, name)
              for name, exts in CONFIG["GROUPS"].items()
              for ext in exts}


class File:
    """Reprensentation of File to arrange"""

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"File(path={self.path})"

    @property
    def name(self) -> str:
        """File name."""
        return self.fullname.rsplit(".", 1)[0]

    @property
    def ext(self) -> str:
        """File extension."""
        return self.fullname[len(self.name) + 1:]

    @property
    def fullname(self) -> str:
        """File name with extension."""
        return os.path.split(self.path)[1]

    @property
    def output(self) -> str:
        """Output dir of extension."""
        return EXT_OUTPUT.get(self.ext.lower(), f"{OUTPUT}/others/")

    @property
    def ignored(self) -> bool:
        """
        Return True if `self.path` is not a file
        or is ignored file or extension.
        """
        return (not os.path.isfile(self.path)
                or self.fullname in IGNORE_FILES
                or self.ext.lower() in IGNORE_EXTENSIONS)

    def arrange(self) -> None:
        """Move `File` in `self.output`."""
        if self.ignored:
            return
        self.move_to(self.output)

    def move_to(self, dest_dir: str) -> None:
        """Move file to `dest_dir` and rename it if requisite."""
        mkdir_if_not_exist(dest_dir)
        try:
            # Try to move it without rename
            dest = os.path.join(dest_dir, self.fullname)
            shutil.move(self.path, os.path.join(dest_dir, self.fullname))
        except FileExistsError:
            # Search count
            try:
                if self.name[-1] == ")":
                    temp = self.name[:-1].rsplit("(", -1)
                    count = int(temp[1])
                    name = temp[0]
                else:
                    raise ValueError("No ')' at end")
            except (ValueError, IndexError):
                count = 0
                name = f"{self.name}" if self.name[-1] == " " else self.name
            ext = f".{self.ext}" if self.ext is not None else ""

            # Loop until file free name with incremented count
            while True:
                count += 1
                fullname = f"{name}({count}){ext}"
                dest = os.path.join(dest_dir, fullname)
                try:
                    os.rename(self.path, dest)
                    break
                except FileExistsError:
                    pass

        # Change file path
        self.path = dest


def mkdir_if_not_exist(path: str) -> None:
    """Create dir at `path` if not exist."""
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def arrange_desktop() -> int:
    """Arrange all non-ignored files and return the moved file count."""
    mkdir_if_not_exist(OUTPUT)
    count = 0
    files = [File(os.path.join(BUREAU, path)) for path in os.listdir(BUREAU)]
    for file in files:
        if not file.ignored:
            file.arrange()
            count += 1
    return count


if __name__ == "__main__":
    arranged = arrange_desktop()
    print(f"{arranged} files aranged")
