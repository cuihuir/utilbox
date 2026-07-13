"""Shared fonts and bundled visual resources for the desktop UI."""
import sys
from pathlib import Path

import customtkinter as ctk
from PIL import Image


UI_FONT_FAMILY = "Noto Sans CJK SC"
UI_MONO_FONT_FAMILY = "Noto Sans Mono CJK SC"
# CustomTkinter applies the first color in light mode and the second in dark mode.
APP_BG = ("#F2F2F7", "#101114")
SURFACE = ("#FFFFFF", "#1C1C1E")
INK = ("#1C1C1E", "#F5F5F7")
SECONDARY = ("#6D6D73", "#A1A1A6")
SEPARATOR = ("#E5E5EA", "#38383A")
PRIMARY = ("#007AFF", "#0A84FF")
PRIMARY_HOVER = ("#0067D8", "#409CFF")
SUCCESS = ("#34C759", "#30D158")
DESTRUCTIVE = ("#FF3B30", "#FF453A")
HEADER_BG = ("#F8F8FA", "#161618")
HOVER_SURFACE = ("#EDEDF2", "#2C2C2E")
CONTROL_FILL = ("#E5E5EA", "#2C2C2E")
CONTROL_HOVER = ("#D1D1D6", "#3A3A3C")
INPUT_BG = ("#FFFFFF", "#2C2C2E")
TERMINAL_BG = ("#1C1C1E", "#000000")
ON_PRIMARY = ("#FFFFFF", "#FFFFFF")
CHEVRON = ("#C7C7CC", "#636366")
PAGE_MARGIN = 32
SECTION_INSET = 8
ROW_INSET = 20
MAX_CONTENT_WIDTH = 836


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
        source = source.convert("RGBA")
        image = Image.new("RGBA", source.size, "#FFFFFF")
        image.putalpha(source.getchannel("A"))
    return ctk.CTkImage(light_image=image, dark_image=image, size=(size, size))
