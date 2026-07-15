from pathlib import Path

import qrcode


class QrGenerator:
    """Generate local PNG QR codes without network access."""

    def build(self, content: str, size: int = 10):
        if not content.strip():
            raise ValueError("二维码内容不能为空")
        return qrcode.make(content.strip(), box_size=size, border=4)

    def generate(self, content: str, output_path: str | Path, size: int = 10) -> Path:
        output = Path(output_path)
        image = self.build(content, size)
        image.save(output)
        return output
