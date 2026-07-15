"""Read UtilBox's single-source version in source and frozen builds."""
import sys
from importlib.metadata import version as installed_version
from pathlib import Path


def _version_file():
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "VERSION"
    return Path(__file__).resolve().parent.parent / "VERSION"


try:
    __version__ = _version_file().read_text(encoding="ascii").strip()
except FileNotFoundError:
    __version__ = installed_version("utilbox")
