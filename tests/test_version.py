"""Regression checks for the single-source application version."""
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from version import __version__


class VersionTests(unittest.TestCase):
    def test_runtime_version_comes_from_the_version_file(self):
        self.assertEqual(__version__, (ROOT / "VERSION").read_text(encoding="ascii").strip())

    def test_version_uses_semantic_versioning(self):
        self.assertRegex(__version__, r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
