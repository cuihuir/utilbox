import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from image_processor import ImageProcessor
from qr_generator import QrGenerator


class ToolCoreTests(unittest.TestCase):
    def test_qr_generator_writes_png(self):
        output = Path("/tmp/utilbox-test-qr.png")
        QrGenerator().generate("https://example.com", output)
        self.assertTrue(output.is_file())

    def test_image_processor_converts_to_webp(self):
        output = Path("/tmp/utilbox-test-image.webp")
        ImageProcessor().process("examples/fishes.png", output, "WEBP", 75)
        self.assertTrue(output.is_file())

    def test_qr_generator_builds_preview_image(self):
        self.assertGreater(QrGenerator().build("preview").width, 0)

    def test_image_processor_reports_batch_result(self):
        results = ImageProcessor().process_many(["examples/fishes.png"], "/tmp/utilbox-batch", "JPEG", 75)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]["output"].is_file())
