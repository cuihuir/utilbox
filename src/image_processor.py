from pathlib import Path

from PIL import Image


class ImageProcessor:
    """Compress and convert raster images locally."""

    def process(self, input_path: str | Path, output_path: str | Path, output_format: str, quality: int) -> Path:
        output = Path(output_path)
        with Image.open(input_path) as image:
            if output_format.upper() in {"JPEG", "JPG"} and image.mode in {"RGBA", "P"}:
                image = image.convert("RGB")
            image.save(output, format=output_format.upper(), quality=quality, optimize=True)
        return output

    def process_many(self, inputs, output_dir: str | Path, output_format: str, quality: int):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        extension = {"JPEG": ".jpg", "JPG": ".jpg", "PNG": ".png", "WEBP": ".webp"}[output_format.upper()]
        results = []
        for input_path in inputs:
            source = Path(input_path)
            target = output_dir / f"{source.stem}{extension}"
            self.process(source, target, output_format, quality)
            results.append({"input": source, "output": target, "before": source.stat().st_size, "after": target.stat().st_size})
        return results
