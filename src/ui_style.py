"""Shared fonts and bundled visual resources for the desktop UI."""
import sys
from pathlib import Path

import customtkinter as ctk
from PIL import Image


UI_FONT_FAMILY = "Noto Sans CJK SC"
UI_MONO_FONT_FAMILY = "Noto Sans Mono CJK SC"


def ui_font(size, weight="normal"):
    """Create the CJK-capable font used for application labels and buttons."""
    return ctk.CTkFont(family=UI_FONT_FAMILY, size=size, weight=weight)


def ui_mono_font(size):
    """Create the CJK-capable monospaced font used in scan results."""
    return ctk.CTkFont(family=UI_MONO_FONT_FAMILY, size=size)


def icon_path(name):
    """Return a bundled icon path in source and PyInstaller environments."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_path / "assets" / "icons" / f"{name}.png"


def load_icon(name, size):
    """Load a bundled icon as a CustomTkinter image at the requested size."""
    with Image.open(icon_path(name)) as source:
        image = source.convert("RGBA")
    return ctk.CTkImage(light_image=image, dark_image=image, size=(size, size))
