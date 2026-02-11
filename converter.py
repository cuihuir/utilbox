"""图片转ICO格式转换器核心逻辑"""
from PIL import Image
from pathlib import Path
from typing import List, Tuple


class ImageConverter:
    """图片转ICO转换器"""

    # 支持的输入格式
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

    # 标准ICO尺寸
    STANDARD_SIZES = [16, 32, 48, 64, 128, 256]

    def __init__(self):
        self.last_error = None

    def validate_image(self, image_path: str) -> bool:
        """验证图片文件是否有效"""
        try:
            path = Path(image_path)

            # 检查文件是否存在
            if not path.exists():
                self.last_error = "文件不存在"
                return False

            # 检查文件扩展名
            if path.suffix.lower() not in self.SUPPORTED_FORMATS:
                self.last_error = f"不支持的格式，仅支持: {', '.join(self.SUPPORTED_FORMATS)}"
                return False

            # 尝试打开图片
            with Image.open(image_path) as img:
                img.verify()

            return True

        except Exception as e:
            self.last_error = f"图片验证失败: {str(e)}"
            return False

    def convert_to_ico(
        self,
        input_path: str,
        output_path: str,
        sizes: List[int] = None
    ) -> Tuple[bool, str]:
        """
        将图片转换为ICO格式

        Args:
            input_path: 输入图片路径
            output_path: 输出ICO文件路径
            sizes: ICO包含的尺寸列表，默认为所有标准尺寸

        Returns:
            (成功标志, 消息)
        """
        try:
            # 验证输入文件
            if not self.validate_image(input_path):
                return False, self.last_error

            # 使用默认尺寸
            if sizes is None or len(sizes) == 0:
                sizes = self.STANDARD_SIZES

            # 确保尺寸按从小到大排序
            sizes = sorted(sizes)

            # 打开原始图片
            with Image.open(input_path) as img:
                # 转换为RGBA模式（ICO需要）
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # 保存为ICO格式，让Pillow自动生成多尺寸
                # 注意：不要手动resize，直接传sizes参数
                img.save(
                    output_path,
                    format='ICO',
                    sizes=[(size, size) for size in sizes]
                )

            return True, f"成功转换为ICO，包含 {len(sizes)} 个尺寸"

        except Exception as e:
            error_msg = f"转换失败: {str(e)}"
            self.last_error = error_msg
            return False, error_msg

    def get_image_info(self, image_path: str) -> dict:
        """获取图片信息"""
        try:
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'size_kb': Path(image_path).stat().st_size / 1024
                }
        except Exception as e:
            return {'error': str(e)}
