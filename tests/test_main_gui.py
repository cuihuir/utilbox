import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main_gui import UI_FONT_FAMILY


class MainGuiFontTests(unittest.TestCase):
    def test_ui_font_uses_noto_sans_cjk_sc(self):
        self.assertEqual(UI_FONT_FAMILY, "Noto Sans CJK SC")
