"""测试转换器核心功能"""
import sys
from pathlib import Path

# 添加父目录到路径以便导入模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from converter import ImageConverter


def test_conversion():
    """测试图片转换功能"""
    converter = ImageConverter()

    # 测试文件（相对于项目根目录）
    project_root = Path(__file__).parent.parent
    test_files = [
        project_root / "examples/fishes.png",
        project_root / "examples/river.png"
    ]

    print("=" * 50)
    print("PNG to ICO 转换器测试")
    print("=" * 50)

    for test_file in test_files:
        if not test_file.exists():
            print(f"\n❌ 文件不存在: {test_file}")
            continue

        print(f"\n📁 测试文件: {test_file.name}")

        # 获取图片信息
        info = converter.get_image_info(str(test_file))
        print(f"   尺寸: {info['width']}x{info['height']}")
        print(f"   格式: {info['format']}")
        print(f"   大小: {info['size_kb']:.1f} KB")

        # 转换为ICO
        output_file = test_file.parent / f"{test_file.stem}_output.ico"
        sizes = [16, 32, 48, 64, 128, 256]

        print(f"   转换尺寸: {sizes}")
        success, message = converter.convert_to_ico(
            str(test_file),
            str(output_file),
            sizes
        )

        if success:
            output_size = output_file.stat().st_size / 1024
            print(f"   ✅ {message}")
            print(f"   输出文件: {output_file.name} ({output_size:.1f} KB)")
        else:
            print(f"   ❌ {message}")

    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    test_conversion()
