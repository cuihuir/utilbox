import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ui_style import APP_BG, PRIMARY, SURFACE, UI_FONT_FAMILY, icon_path


class UiStyleTests(unittest.TestCase):
    def test_ui_font_uses_noto_sans_cjk_sc(self):
        self.assertEqual(UI_FONT_FAMILY, "Noto Sans CJK SC")

    def test_bundled_tool_icons_exist(self):
        self.assertTrue(icon_path("image-converter").is_file())
        self.assertTrue(icon_path("network-scan").is_file())

    def test_ios_style_uses_light_surface_tokens(self):
        self.assertEqual(APP_BG, ("#F2F2F7", "#101114"))
        self.assertEqual(SURFACE, ("#FFFFFF", "#1C1C1E"))
        self.assertEqual(PRIMARY, ("#007AFF", "#0A84FF"))
